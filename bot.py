"""Binance Spot Trading Bot - Core Bot Class
Handles all trading operations and API interactions
"""

import logging
import os
from typing import Dict, Optional, Union
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BasicBot:
    """
    A basic trading bot for Binance Spot Testnet
    Supports MARKET and LIMIT orders for BUY/SELL operations
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """Initialize the bot with API credentials and logging"""
        self.setup_logging()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        
        # Validate API credentials
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not found. Please check your .env file.")
        
        # Initialize Binance client for Spot Testnet
        self.client = self._initialize_client(testnet)
        
        # Test connection
        self._test_connection()
        
    def setup_logging(self):
        """Configure logging for the bot"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _initialize_client(self, testnet: bool) -> Client:
        """Initialize and return Binance client for Spot Testnet"""
        try:
            client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True  # Enable testnet mode
            )
            
            # Set to Spot Testnet mode
            if testnet:
                client.API_URL = 'https://testnet.binance.vision/api'
            
            self.logger.info("Successfully initialized Binance Spot Testnet client")
            return client
            
        except Exception as e:
            self.logger.error(f"Failed to initialize client: {e}")
            raise
            
    def _test_connection(self):
        """Test the connection to Binance Spot API"""
        try:
            # Test connectivity
            server_time = self.client.get_server_time()
            self.logger.info(f"Connected to Binance Spot Testnet. Server time: {server_time}")
            
            # Test account access
            account_info = self.client.get_account()
            self.logger.info("Account access verified")
            
        except BinanceAPIException as e:
            self.logger.error(f"API connection failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            raise
            
    def get_account_balance(self) -> Dict:
        """Get current account balance"""
        try:
            account_info = self.client.get_account()
            balance = account_info['balances']
            self.logger.info("Retrieved account balance")
            return balance
        except Exception as e:
            self.logger.error(f"Failed to get account balance: {e}")
            raise
            
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get symbol information and trading rules"""
        try:
            exchange_info = self.client.get_exchange_info()
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol.upper():
                    self.logger.info(f"Retrieved info for {symbol}")
                    return symbol_info
            raise ValueError(f"Symbol {symbol} not found")
        except Exception as e:
            self.logger.error(f"Failed to get symbol info: {e}")
            raise
            
    def place_order(self, 
                   symbol: str, 
                   side: str, 
                   order_type: str, 
                   quantity: float, 
                   price: Optional[float] = None,
                   stop_price: Optional[float] = None,
                   time_in_force: str = TIME_IN_FORCE_GTC) -> Dict:
        """
        Place a spot order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            order_type: 'MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET'
            quantity: Order quantity
            price: Price for limit orders
            stop_price: Stop price for stop orders
            time_in_force: Time in force for limit orders
            
        Returns:
            Dict containing order information
        """
        try:
            # Validate inputs
            symbol = symbol.upper()
            side = side.upper()
            order_type = order_type.upper()
            
            # Validate side
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
                
            # Validate order type
            valid_order_types = ['MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']
            if order_type not in valid_order_types:
                raise ValueError(f"Order type must be one of: {valid_order_types}")
            
            # Check for sufficient balance
            if side == 'BUY':
                # For BUY orders, check if we have enough quote currency (e.g., USDT)
                quote_asset = symbol[len(symbol)-4:] if symbol.endswith('USDT') else 'USDT'
                base_asset = symbol[:len(symbol)-4] if symbol.endswith('USDT') else symbol[:len(symbol)-3]
                
                # Get account balance
                account_info = self.client.get_account()
                quote_balance = 0
                
                for balance in account_info['balances']:
                    if balance['asset'] == quote_asset:
                        quote_balance = float(balance['free'])
                        break
                
                # Calculate required amount
                if order_type == 'MARKET':
                    # For market orders, estimate using current price
                    current_price = self.get_current_price(symbol)
                    required_amount = quantity * current_price * 1.01  # Add 1% buffer for price movement
                else:
                    # For limit orders, use the specified price
                    required_amount = quantity * price
                
                if quote_balance < required_amount:
                    max_possible = quote_balance / (current_price if order_type == 'MARKET' else price)
                    error_msg = f"Insufficient balance. You have {quote_balance} {quote_asset}, but need approximately {required_amount} {quote_asset}. "
                    error_msg += f"Consider lowering quantity to {max_possible:.6f} {base_asset} or less."
                    raise Exception(error_msg)
            else:  # SELL order
                # For SELL orders, check if we have enough base currency (e.g., BTC)
                base_asset = symbol[:len(symbol)-4] if symbol.endswith('USDT') else symbol[:len(symbol)-3]
                
                # Get account balance
                account_info = self.client.get_account()
                base_balance = 0
                
                for balance in account_info['balances']:
                    if balance['asset'] == base_asset:
                        base_balance = float(balance['free'])
                        break
                
                if base_balance < quantity:
                    error_msg = f"Insufficient balance. You have {base_balance} {base_asset}, but want to sell {quantity} {base_asset}. "
                    error_msg += f"Consider lowering quantity to {base_balance} {base_asset} or less."
                    raise Exception(error_msg)
            
            # Validate price for LIMIT orders (prevent PERCENT_PRICE_BY_SIDE error)
            if order_type == 'LIMIT' and price is not None:
                current_price = self.get_current_price(symbol)
                price_deviation = abs(price - current_price) / current_price * 100
                
                if price_deviation > 20:  # If price is more than 20% away from current price
                    min_price = current_price * 0.8
                    max_price = current_price * 1.2
                    error_msg = f"Price {price} is too far from current market price {current_price} (±20% limit). "
                    error_msg += f"Please use a price between {min_price:.8f} and {max_price:.8f}."
                    raise Exception(error_msg)
            
            # Prepare order parameters
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            
            # Add price for limit orders
            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                order_params['price'] = price
                order_params['timeInForce'] = time_in_force
                
            # Add stop price for stop orders
            if order_type in ['STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']:
                if stop_price is None:
                    raise ValueError(f"Stop price is required for {order_type} orders")
                order_params['stopPrice'] = stop_price
                
            # Log order attempt
            self.logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
            if self.debug_mode:
                self.logger.debug(f"Order parameters: {order_params}")
            
            # Place the order
            order_response = self.client.create_order(**order_params)
            
            # Log successful order
            self.logger.info(f"Order placed successfully. Order ID: {order_response['orderId']}")
            
            # Get order details
            order_details = self.get_order_details(symbol, order_response['orderId'])
            
            return {
                'order_response': order_response,
                'order_details': order_details
            }
            
        except BinanceAPIException as e:
            error_msg = f"Binance API error: {e.message} (Code: {e.code})"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except BinanceOrderException as e:
            error_msg = f"Order error: {e.message} (Code: {e.code})"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Failed to place order: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
    def get_order_details(self, symbol: str, order_id: int) -> Dict:
        """Get details of a specific order"""
        try:
            order_details = self.client.get_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            return order_details
        except Exception as e:
            self.logger.error(f"Failed to get order details: {e}")
            raise
            
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an open order"""
        try:
            cancel_response = self.client.cancel_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            self.logger.info(f"Order {order_id} cancelled successfully")
            return cancel_response
        except Exception as e:
            self.logger.error(f"Failed to cancel order: {e}")
            raise
            
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """Get all open orders or open orders for a specific symbol"""
        try:
            if symbol:
                orders = self.client.get_open_orders(symbol=symbol.upper())
            else:
                orders = self.client.get_open_orders()
            
            self.logger.info(f"Retrieved {len(orders)} open orders")
            return orders
        except Exception as e:
            self.logger.error(f"Failed to get open orders: {e}")
            raise
            
    def get_position_info(self, symbol: Optional[str] = None) -> list:
        """Get position information (holdings in spot)"""
        try:
            account_info = self.client.get_account()
            balances = account_info['balances']
            
            # Filter out assets with zero balance
            active_positions = []
            for balance in balances:
                free_amount = float(balance['free'])
                locked_amount = float(balance['locked'])
                total_amount = free_amount + locked_amount
                
                if total_amount > 0:
                    # If symbol is specified, filter by that symbol
                    if symbol is None or balance['asset'] in symbol.upper() or balance['asset'] + 'USDT' == symbol.upper():
                        active_positions.append({
                            'asset': balance['asset'],
                            'free': balance['free'],
                            'locked': balance['locked'],
                            'total': str(total_amount)
                        })
            
            self.logger.info(f"Retrieved {len(active_positions)} active positions")
            return active_positions
        except Exception as e:
            self.logger.error(f"Failed to get position info: {e}")
            raise
            
    def get_current_price(self, symbol: str) -> float:
        """Get current market price for a symbol"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol.upper())
            price = float(ticker['price'])
            self.logger.info(f"Current price for {symbol}: {price}")
            return price
        except Exception as e:
            self.logger.error(f"Failed to get current price: {e}")
            raise
            
    def format_order_summary(self, order_info: Dict) -> str:
        """Format order information for display"""
        order_details = order_info['order_details']
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                   ORDER SUMMARY                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║ Order ID: {order_details['orderId']:<20} │ Status: {order_details['status']:<20} ║
║ Symbol: {order_details['symbol']:<22} │ Side: {order_details['side']:<22} ║
║ Type: {order_details['type']:<24} │ Quantity: {order_details['origQty']:<19} ║
║ Price: {order_details.get('price', 'N/A'):<23} │ Filled: {order_details['executedQty']:<20} ║
║ Time: {order_details['time']:<63} ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
        """
        
        return summary.strip()