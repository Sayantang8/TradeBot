"""
Binance Futures Trading Bot - GUI Interface (Optional Bonus)
Simple Tkinter GUI for placing orders and monitoring trades
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from datetime import datetime
from bot import BasicBot

class TradingBotGUI:
    """Simple GUI for the trading bot"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Binance Futures Trading Bot - TESTNET")
        self.root.geometry("900x700")
        
        # Initialize bot
        self.bot = None
        self.init_bot()
        
        # Create GUI
        self.create_widgets()
        
        # Setup logging
        self.setup_logging()
        
    def init_bot(self):
        """Initialize the trading bot"""
        try:
            self.bot = BasicBot()
            self.log_message("✅ Bot initialized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize bot: {e}")
            self.root.destroy()
            return
    
    def setup_logging(self):
        """Setup logging to display in GUI"""
        # Create a custom handler to redirect logs to GUI
        class GUILogHandler(logging.Handler):
            def __init__(self, gui):
                super().__init__()
                self.gui = gui
                
            def emit(self, record):
                msg = self.format(record)
                self.gui.log_message(msg)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        gui_handler = GUILogHandler(self)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(gui_handler)
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_order_tab(notebook)
        self.create_account_tab(notebook)
        self.create_log_tab(notebook)
        
    def create_order_tab(self, notebook):
        """Create the order placement tab"""
        order_frame = ttk.Frame(notebook)
        notebook.add(order_frame, text="Place Order")
        
        # Order form
        form_frame = ttk.LabelFrame(order_frame, text="Order Details", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Symbol
        ttk.Label(form_frame, text="Symbol:").grid(row=0, column=0, sticky='w', pady=5)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        ttk.Entry(form_frame, textvariable=self.symbol_var, width=15).grid(row=0, column=1, sticky='w', pady=5)
        
        # Get price button
        ttk.Button(form_frame, text="Get Price", command=self.get_current_price).grid(row=0, column=2, padx=10, pady=5)
        
        # Current price display
        self.price_label = ttk.Label(form_frame, text="Current Price: N/A")
        self.price_label.grid(row=0, column=3, padx=10, pady=5)
        
        # Side
        ttk.Label(form_frame, text="Side:").grid(row=1, column=0, sticky='w', pady=5)
        self.side_var = tk.StringVar(value="BUY")
        side_combo = ttk.Combobox(form_frame, textvariable=self.side_var, values=["BUY", "SELL"], state="readonly", width=12)
        side_combo.grid(row=1, column=1, sticky='w', pady=5)
        
        # Order Type
        ttk.Label(form_frame, text="Order Type:").grid(row=2, column=0, sticky='w', pady=5)
        self.order_type_var = tk.StringVar(value="MARKET")
        type_combo = ttk.Combobox(form_frame, textvariable=self.order_type_var, values=["MARKET", "LIMIT"], state="readonly", width=12)
        type_combo.grid(row=2, column=1, sticky='w', pady=5)
        type_combo.bind("<<ComboboxSelected>>", self.on_order_type_change)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky='w', pady=5)
        self.quantity_var = tk.StringVar(value="0.001")
        ttk.Entry(form_frame, textvariable=self.quantity_var, width=15).grid(row=3, column=1, sticky='w', pady=5)
        
        # Price (for limit orders)
        ttk.Label(form_frame, text="Price:").grid(row=4, column=0, sticky='w', pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(form_frame, textvariable=self.price_var, width=15, state="disabled")
        self.price_entry.grid(row=4, column=1, sticky='w', pady=5)
        
        # Leverage
        ttk.Label(form_frame, text="Leverage:").grid(row=5, column=0, sticky='w', pady=5)
        self.leverage_var = tk.StringVar(value="1")
        ttk.Entry(form_frame, textvariable=self.leverage_var, width=15).grid(row=5, column=1, sticky='w', pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Place Order", command=self.place_order).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel All Orders", command=self.cancel_all_orders).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Close All Positions", command=self.close_all_positions).pack(side='left', padx=5)
        
        # Order status
        status_frame = ttk.LabelFrame(order_frame, text="Recent Orders", padding=10)
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for orders
        columns = ('Symbol', 'Side', 'Type', 'Quantity', 'Price', 'Status', 'Time')
        self.orders_tree = ttk.Treeview(status_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=100)
        
        # Scrollbar for orders
        orders_scrollbar = ttk.Scrollbar(status_frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=orders_scrollbar.set)
        
        self.orders_tree.pack(side='left', fill='both', expand=True)
        orders_scrollbar.pack(side='right', fill='y')
        
    def create_account_tab(self, notebook):
        """Create the account information tab"""
        account_frame = ttk.Frame(notebook)
        notebook.add(account_frame, text="Account Info")
        
        # Account info
        info_frame = ttk.LabelFrame(account_frame, text="Account Balance", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        # Balance labels
        self.balance_label = ttk.Label(info_frame, text="USDT Balance: Loading...")
        self.balance_label.pack(anchor='w', pady=5)
        
        self.margin_label = ttk.Label(info_frame, text="Available Margin: Loading...")
        self.margin_label.pack(anchor='w', pady=5)
        
        # Refresh button
        ttk.Button(info_frame, text="Refresh Account Info", command=self.refresh_account_info).pack(pady=10)
        
        # Positions
        positions_frame = ttk.LabelFrame(account_frame, text="Open Positions", padding=10)
        positions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for positions
        pos_columns = ('Symbol', 'Side', 'Size', 'Entry Price', 'Mark Price', 'PnL', 'ROE%')
        self.positions_tree = ttk.Treeview(positions_frame, columns=pos_columns, show='headings', height=8)
        
        for col in pos_columns:
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=100)
        
        # Scrollbar for positions
        pos_scrollbar = ttk.Scrollbar(positions_frame, orient='vertical', command=self.positions_tree.yview)
        self.positions_tree.configure(yscrollcommand=pos_scrollbar.set)
        
        self.positions_tree.pack(side='left', fill='both', expand=True)
        pos_scrollbar.pack(side='right', fill='y')
        
    def create_log_tab(self, notebook):
        """Create the log tab"""
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Logs")
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=25)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear logs button
        ttk.Button(log_frame, text="Clear Logs", command=self.clear_logs).pack(pady=5)
        
    def on_order_type_change(self, event):
        """Handle order type change"""
        if self.order_type_var.get() == "LIMIT":
            self.price_entry.config(state="normal")
        else:
            self.price_entry.config(state="disabled")
            self.price_var.set("")
    
    def get_current_price(self):
        """Get current price for the symbol"""
        def _get_price():
            try:
                symbol = self.symbol_var.get().upper()
                if not symbol:
                    return
                
                price = self.bot.get_current_price(symbol)
                self.price_label.config(text=f"Current Price: ${price:,.2f}")
                
                # Auto-fill limit price if in limit mode
                if self.order_type_var.get() == "LIMIT":
                    self.price_var.set(str(price))
                    
            except Exception as e:
                self.log_message(f"❌ Error getting price: {e}")
                messagebox.showerror("Error", f"Failed to get price: {e}")
        
        threading.Thread(target=_get_price, daemon=True).start()
    
    def place_order(self):
        """Place a new order"""
        def _place_order():
            try:
                symbol = self.symbol_var.get().upper()
                side = self.side_var.get()
                order_type = self.order_type_var.get()
                quantity = float(self.quantity_var.get())
                leverage = int(self.leverage_var.get())
                
                if not symbol or quantity <= 0:
                    messagebox.showerror("Error", "Please enter valid symbol and quantity")
                    return
                
                # Set leverage first
                self.bot.set_leverage(symbol, leverage)
                
                # Place order
                if order_type == "MARKET":
                    result = self.bot.place_market_order(symbol, side, quantity)
                else:  # LIMIT
                    price = float(self.price_var.get())
                    if price <= 0:
                        messagebox.showerror("Error", "Please enter valid price for limit order")
                        return
                    result = self.bot.place_limit_order(symbol, side, quantity, price)
                
                if result:
                    self.log_message(f"✅ Order placed successfully: {result.get('orderId', 'N/A')}")
                    self.add_order_to_tree(result)
                    self.refresh_account_info()
                    messagebox.showinfo("Success", "Order placed successfully!")
                
            except Exception as e:
                self.log_message(f"❌ Error placing order: {e}")
                messagebox.showerror("Error", f"Failed to place order: {e}")
        
        threading.Thread(target=_place_order, daemon=True).start()
    
    def cancel_all_orders(self):
        """Cancel all open orders"""
        def _cancel_orders():
            try:
                symbol = self.symbol_var.get().upper()
                if not symbol:
                    messagebox.showerror("Error", "Please enter a symbol")
                    return
                
                result = self.bot.cancel_all_orders(symbol)
                if result:
                    self.log_message(f"✅ All orders cancelled for {symbol}")
                    messagebox.showinfo("Success", f"All orders cancelled for {symbol}")
                    self.refresh_account_info()
                
            except Exception as e:
                self.log_message(f"❌ Error cancelling orders: {e}")
                messagebox.showerror("Error", f"Failed to cancel orders: {e}")
        
        threading.Thread(target=_cancel_orders, daemon=True).start()
    
    def close_all_positions(self):
        """Close all open positions"""
        def _close_positions():
            try:
                result = self.bot.close_all_positions()
                if result:
                    self.log_message("✅ All positions closed")
                    messagebox.showinfo("Success", "All positions closed")
                    self.refresh_account_info()
                
            except Exception as e:
                self.log_message(f"❌ Error closing positions: {e}")
                messagebox.showerror("Error", f"Failed to close positions: {e}")
        
        threading.Thread(target=_close_positions, daemon=True).start()
    
    def refresh_account_info(self):
        """Refresh account information"""
        def _refresh():
            try:
                # Get account info
                account_info = self.bot.get_account_info()
                
                # Update balance
                for asset in account_info.get('assets', []):
                    if asset['asset'] == 'USDT':
                        balance = float(asset['walletBalance'])
                        available = float(asset['availableBalance'])
                        self.balance_label.config(text=f"USDT Balance: {balance:.2f}")
                        self.margin_label.config(text=f"Available Margin: {available:.2f}")
                        break
                
                # Update positions
                self.update_positions_tree(account_info.get('positions', []))
                
            except Exception as e:
                self.log_message(f"❌ Error refreshing account info: {e}")
        
        threading.Thread(target=_refresh, daemon=True).start()
    
    def update_positions_tree(self, positions):
        """Update positions tree view"""
        # Clear existing items
        for item in self.positions_tree.get_children():
            self.positions_tree.delete(item)
        
        # Add active positions
        for pos in positions:
            if float(pos['positionAmt']) != 0:
                side = "LONG" if float(pos['positionAmt']) > 0 else "SHORT"
                size = abs(float(pos['positionAmt']))
                entry_price = float(pos['entryPrice'])
                mark_price = float(pos['markPrice'])
                pnl = float(pos['unRealizedProfit'])
                roe = float(pos['percentage'])
                
                self.positions_tree.insert('', 'end', values=(
                    pos['symbol'],
                    side,
                    f"{size:.6f}",
                    f"${entry_price:,.2f}",
                    f"${mark_price:,.2f}",
                    f"${pnl:,.2f}",
                    f"{roe:.2f}%"
                ))
    
    def add_order_to_tree(self, order):
        """Add order to the orders tree"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        self.orders_tree.insert('', 0, values=(
            order.get('symbol', 'N/A'),
            order.get('side', 'N/A'),
            order.get('type', 'N/A'),
            order.get('origQty', 'N/A'),
            order.get('price', 'N/A'),
            order.get('status', 'N/A'),
            current_time
        ))
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Use after_idle to ensure thread safety
        self.root.after_idle(lambda: self._append_log(log_message))
    
    def _append_log(self, message):
        """Append message to log text widget"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.get('1.0', tk.END).count('\n')
        if lines > 1000:
            self.log_text.delete('1.0', '100.0')
    
    def clear_logs(self):
        """Clear all logs"""
        self.log_text.delete('1.0', tk.END)
    
    def run(self):
        """Run the GUI application"""
        # Initial account info refresh
        self.root.after(1000, self.refresh_account_info)
        
        # Start main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = TradingBotGUI()
    app.run()