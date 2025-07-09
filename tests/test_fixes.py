#!/usr/bin/env python3
"""
Test script to verify the fixes made to the Binance Spot Testnet trading bot
"""

import logging
import sys
from bot import BasicBot
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_balance_command():
    """Test the fixed balance command"""
    logger.info("\n===== Testing balance command =====")
    try:
        bot = BasicBot()
        balances = bot.get_account_balance()
        
        # Check if balances is a list
        if not isinstance(balances, list):
            logger.error(f"Expected balances to be a list, got {type(balances)}")
            return False
            
        # Check if each balance has the expected keys
        for balance in balances:
            if not all(key in balance for key in ['asset', 'free', 'locked']):
                logger.error(f"Balance missing required keys: {balance}")
                return False
                
        logger.info("Balance command test passed")
        return True
    except Exception as e:
        logger.error(f"Balance command test failed: {e}")
        return False

def test_holdings_command():
    """Test the fixed holdings (positions) command"""
    logger.info("\n===== Testing holdings command =====")
    try:
        bot = BasicBot()
        holdings = bot.get_position_info()
        
        # Check if holdings is a list
        if not isinstance(holdings, list):
            logger.error(f"Expected holdings to be a list, got {type(holdings)}")
            return False
            
        # Check if each holding has the expected keys
        for holding in holdings:
            if not all(key in holding for key in ['asset', 'free', 'locked', 'total']):
                logger.error(f"Holding missing required keys: {holding}")
                return False
                
        logger.info("Holdings command test passed")
        return True
    except Exception as e:
        logger.error(f"Holdings command test failed: {e}")
        return False

def test_insufficient_balance_check():
    """Test the insufficient balance check"""
    logger.info("\n===== Testing insufficient balance check =====")
    try:
        bot = BasicBot()
        
        # Try to buy a large amount of BTC (should fail with insufficient balance)
        try:
            bot.place_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity=100  # Very large quantity that should exceed balance
            )
            logger.error("Expected insufficient balance error, but order was placed")
            return False
        except Exception as e:
            if "Insufficient balance" in str(e):
                logger.info("Insufficient balance check passed")
                return True
            else:
                logger.error(f"Expected insufficient balance error, got: {e}")
                return False
    except Exception as e:
        logger.error(f"Insufficient balance check test failed: {e}")
        return False

def test_limit_price_validation():
    """Test the limit price validation"""
    logger.info("\n===== Testing limit price validation =====")
    try:
        bot = BasicBot()
        
        # Get current price of BTCUSDT
        current_price = bot.get_current_price("BTCUSDT")
        logger.info(f"Current BTCUSDT price: {current_price}")
        
        # Try to place a limit order with price 50% below current price (should fail)
        try:
            bot.place_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                quantity=0.001,
                price=current_price * 0.5  # 50% below current price
            )
            logger.error("Expected price validation error, but order was placed")
            return False
        except Exception as e:
            if "too far from current market price" in str(e):
                logger.info("Limit price validation check passed")
                return True
            else:
                logger.error(f"Expected price validation error, got: {e}")
                return False
    except Exception as e:
        logger.error(f"Limit price validation test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting tests for Binance Spot Testnet trading bot fixes")
    
    tests = [
        test_balance_command,
        test_holdings_command,
        test_insufficient_balance_check,
        test_limit_price_validation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Print summary
    logger.info("\n===== Test Summary =====")
    for i, test in enumerate(tests):
        status = "PASSED" if results[i] else "FAILED"
        logger.info(f"{test.__name__}: {status}")
    
    # Overall result
    if all(results):
        logger.info("All tests passed!")
        return 0
    else:
        logger.error("Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())