"""Test script for Binance Spot Testnet

This script tests the modified bot by placing a market order for BTCUSDT
"""

import logging
from bot import BasicBot

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize the bot
        logger.info("Initializing Binance Spot Testnet bot...")
        bot = BasicBot()
        
        # Check account balance
        logger.info("Checking account balance...")
        balances = bot.get_account_balance()
        for balance in balances:
            if float(balance['free']) > 0 or float(balance['locked']) > 0:
                logger.info(f"Asset: {balance['asset']}, Free: {balance['free']}, Locked: {balance['locked']}")
        
        # Get current price of BTCUSDT
        symbol = "BTCUSDT"
        logger.info(f"Getting current price for {symbol}...")
        price = bot.get_current_price(symbol)
        logger.info(f"Current price for {symbol}: ${price}")
        
        # Place a market order to buy a small amount of BTC
        logger.info("Placing a market order...")
        order_result = bot.place_order(
            symbol=symbol,
            side="BUY",
            order_type="MARKET",
            quantity=0.001  # Small amount of BTC
        )
        
        # Print order details
        logger.info("Order placed successfully!")
        logger.info(bot.format_order_summary(order_result))
        
        # Check updated balance
        logger.info("Checking updated account balance...")
        updated_balances = bot.get_account_balance()
        for balance in updated_balances:
            if balance['asset'] in ['BTC', 'USDT'] and (float(balance['free']) > 0 or float(balance['locked']) > 0):
                logger.info(f"Asset: {balance['asset']}, Free: {balance['free']}, Locked: {balance['locked']}")
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()