"""Binance Spot Trading Bot - Command Line Interface
Provides interactive CLI for placing orders and managing trades
"""

import argparse
import sys
import logging
from typing import Optional
from bot import BasicBot

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                          BINANCE SPOT TRADING BOT                                   ║
║                                (TESTNET MODE)                                       ║
║                                                                                      ║
║  ⚠️  WARNING: This is for TESTNET only. No real money involved.                    ║
║  💡  Always test thoroughly before using with real funds.                          ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """Print available commands"""
    help_text = """
Available Commands:
  place     - Place a new order
  balance   - Check account balance
  holdings  - View current asset holdings
  orders    - View open orders
  cancel    - Cancel an order
  price     - Get current price
  help      - Show this help message
  exit      - Exit the bot
"""
    print(help_text)

def get_user_input(prompt: str, input_type: type = str, required: bool = True):
    """Get user input with type validation"""
    while True:
        try:
            value = input(prompt)
            if not value and required:
                print("This field is required. Please enter a value.")
                continue
            if not value and not required:
                return None
            return input_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def place_order_interactive(bot: BasicBot):
    """Interactive order placement"""
    print("\n" + "="*50)
    print("           PLACE ORDER")
    print("="*50)
    
    # Get symbol
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ").upper()
    if not symbol:
        return
    
    # Get current price for reference
    try:
        current_price = bot.get_current_price(symbol)
        print(f"Current price for {symbol}: ${current_price}")
    except Exception as e:
        print(f"Warning: Could not get current price - {e}")
    
    # Get order side
    print("\nOrder Side:")
    print("1. BUY")
    print("2. SELL")
    side_choice = get_user_input("Choose side (1 or 2): ", int)
    if side_choice not in [1, 2]:
        print("Invalid choice.")
        return
    side = "BUY" if side_choice == 1 else "SELL"
    
    # Get order type
    print("\nOrder Type:")
    print("1. MARKET")
    print("2. LIMIT")
    print("3. STOP_MARKET")
    print("4. STOP (Stop-Limit)")
    type_choice = get_user_input("Choose order type (1-4): ", int)
    
    order_type_map = {
        1: "MARKET",
        2: "LIMIT", 
        3: "STOP_MARKET",
        4: "STOP"
    }
    
    if type_choice not in order_type_map:
        print("Invalid choice.")
        return
    
    order_type = order_type_map[type_choice]
    
    # Get quantity
    quantity = get_user_input("Enter quantity: ", float)
    if not quantity or quantity <= 0:
        print("Invalid quantity.")
        return
    
    # Get price for limit orders
    price = None
    if order_type in ["LIMIT", "STOP"]:
        price = get_user_input("Enter price: ", float)
        if not price or price <= 0:
            print("Invalid price.")
            return
    
    # Get stop price for stop orders
    stop_price = None
    if order_type in ["STOP_MARKET", "STOP"]:
        stop_price = get_user_input("Enter stop price: ", float)
        if not stop_price or stop_price <= 0:
            print("Invalid stop price.")
            return
    
    # Confirm order
    print("\n" + "-"*50)
    print("ORDER CONFIRMATION")
    print("-"*50)
    print(f"Symbol: {symbol}")
    print(f"Side: {side}")
    print(f"Type: {order_type}")
    print(f"Quantity: {quantity}")
    if price:
        print(f"Price: {price}")
    if stop_price:
        print(f"Stop Price: {stop_price}")
    print("-"*50)
    
    confirm = get_user_input("Confirm order? (y/n): ").lower()
    if confirm != 'y':
        print("Order cancelled.")
        return
    
    # Place the order
    try:
        print("\nPlacing order...")
        order_info = bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        print("\n✅ ORDER PLACED SUCCESSFULLY!")
        print(bot.format_order_summary(order_info))
        
    except Exception as e:
        print(f"\n❌ ORDER FAILED: {e}")

def show_balance(bot: BasicBot):
    """Show account balance"""
    try:
        balances = bot.get_account_balance()
        print("\n" + "="*50)
        print("           ACCOUNT BALANCE")
        print("="*50)
        
        has_balance = False
        for asset in balances:
            if float(asset['free']) > 0 or float(asset['locked']) > 0:
                has_balance = True
                total = float(asset['free']) + float(asset['locked'])
                print(f"{asset['asset']}: {total:.8f} (Free: {asset['free']}, Locked: {asset['locked']})")
        
        if not has_balance:
            print("No assets with balance.")
                
    except Exception as e:
        print(f"Error getting balance: {e}")

def show_holdings(bot: BasicBot):
    """Show current asset holdings"""
    try:
        holdings = bot.get_position_info()
        print("\n" + "="*50)
        print("           CURRENT HOLDINGS")
        print("="*50)
        
        if not holdings:
            print("No assets held.")
            return
            
        for asset in holdings:
            print(f"Asset: {asset['asset']}")
            print(f"Total: {asset['total']}")
            print(f"Free: {asset['free']}")
            print(f"Locked: {asset['locked']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error getting holdings: {e}")

def show_orders(bot: BasicBot):
    """Show open orders"""
    try:
        orders = bot.get_open_orders()
        print("\n" + "="*50)
        print("           OPEN ORDERS")
        print("="*50)
        
        if not orders:
            print("No open orders.")
            return
            
        for order in orders:
            print(f"Order ID: {order['orderId']}")
            print(f"Symbol: {order['symbol']}")
            print(f"Side: {order['side']}")
            print(f"Type: {order['type']}")
            print(f"Quantity: {order['origQty']}")
            print(f"Price: {order.get('price', 'N/A')}")
            print(f"Status: {order['status']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error getting orders: {e}")

def cancel_order_interactive(bot: BasicBot):
    """Interactive order cancellation"""
    print("\n" + "="*50)
    print("           CANCEL ORDER")
    print("="*50)
    
    # Show open orders first
    try:
        orders = bot.get_open_orders()
        if not orders:
            print("No open orders to cancel.")
            return
            
        print("Open orders:")
        for i, order in enumerate(orders):
            print(f"{i+1}. Order ID: {order['orderId']} - {order['symbol']} {order['side']} {order['type']}")
            
    except Exception as e:
        print(f"Error getting orders: {e}")
        return
    
    # Get order to cancel
    try:
        choice = get_user_input("Enter order number to cancel (or 0 to go back): ", int)
        if choice == 0:
            return
        if choice < 1 or choice > len(orders):
            print("Invalid choice.")
            return
            
        order_to_cancel = orders[choice - 1]
        
        # Confirm cancellation
        confirm = get_user_input(f"Cancel order {order_to_cancel['orderId']}? (y/n): ").lower()
        if confirm != 'y':
            print("Cancellation aborted.")
            return
            
        # Cancel the order
        result = bot.cancel_order(order_to_cancel['symbol'], order_to_cancel['orderId'])
        print(f"✅ Order {order_to_cancel['orderId']} cancelled successfully!")
        
    except Exception as e:
        print(f"❌ Error cancelling order: {e}")

def get_price_interactive(bot: BasicBot):
    """Get current price for a symbol"""
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ").upper()
    if not symbol:
        return
        
    try:
        price = bot.get_current_price(symbol)
        print(f"\nCurrent price for {symbol}: ${price}")
    except Exception as e:
        print(f"Error getting price: {e}")

def run_cli_mode():
    """Run the bot in interactive CLI mode"""
    print_banner()
    
    # Initialize bot
    try:
        bot = BasicBot()
        print("✅ Bot initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        return
    
    print_help()
    
    # Main command loop
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'exit':
                print("Goodbye!")
                break
            elif command == 'help':
                print_help()
            elif command == 'place':
                place_order_interactive(bot)
            elif command == 'balance':
                show_balance(bot)
            elif command == 'holdings' or command == 'positions':
                show_holdings(bot)
            elif command == 'orders':
                show_orders(bot)
            elif command == 'cancel':
                cancel_order_interactive(bot)
            elif command == 'price':
                get_price_interactive(bot)
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_single_command(args):
    """Run a single command with arguments"""
    try:
        bot = BasicBot()
        
        order_info = bot.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        
        print("✅ ORDER PLACED SUCCESSFULLY!")
        print(bot.format_order_summary(order_info))
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot for Testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--symbol', '-s', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', '-t', choices=['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP'], 
                       help='Order type')
    parser.add_argument('--quantity', '-q', type=float, help='Order quantity')
    parser.add_argument('--price', '-p', type=float, help='Order price (for LIMIT orders)')
    parser.add_argument('--stop-price', type=float, help='Stop price (for STOP orders)')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # If no arguments or interactive flag, run CLI mode
    if len(sys.argv) == 1 or args.interactive:
        run_cli_mode()
    else:
        # Validate required arguments for single command
        if not all([args.symbol, args.side, args.type, args.quantity]):
            print("Error: symbol, side, type, and quantity are required for single command mode.")
            print("Use --interactive or -i for interactive mode.")
            sys.exit(1)
            
        # Validate price for LIMIT orders
        if args.type in ['LIMIT', 'STOP'] and not args.price:
            print("Error: price is required for LIMIT and STOP orders.")
            sys.exit(1)
            
        # Validate stop price for STOP orders  
        if args.type in ['STOP_MARKET', 'STOP'] and not args.stop_price:
            print("Error: stop-price is required for STOP orders.")
            sys.exit(1)
            
        run_single_command(args)

if __name__ == "__main__":
    main()