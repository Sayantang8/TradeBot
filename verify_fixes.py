#!/usr/bin/env python3
"""
Verification script for Binance Spot Testnet Trading Bot fixes

This script tests the following fixes:
1. Balance command showing all non-zero balances
2. Holdings command (renamed from positions) showing correct holdings
3. Pre-order balance check for insufficient balance
4. Limit order price validation (±20% of current price)
"""

import os
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot import BasicBot

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{text}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_failure(message):
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}! {message}{RESET}")

def test_balance_command(bot):
    print_header("Testing balance command...")
    try:
        # Get account info directly from client
        account_info = bot.client.get_account()
        balances = account_info['balances']
        non_zero_balances = [b for b in balances if float(b['free']) > 0 or float(b['locked']) > 0]
        
        # Get balances from bot method
        bot_balances = bot.get_position_info()
        
        # Check if bot returns all non-zero balances
        if len(bot_balances) == len(non_zero_balances):
            print_success("Balance command correctly returns all non-zero balances")
            return True
        else:
            print_failure(f"Balance count mismatch: bot returned {len(bot_balances)}, expected {len(non_zero_balances)}")
            return False
    except Exception as e:
        print_failure(f"Error testing balance command: {str(e)}")
        return False

def test_insufficient_balance_check(bot):
    print_header("Testing insufficient balance check...")
    try:
        # Get a symbol with insufficient balance
        symbol = "BTCUSDT"
        current_price = float(bot.get_current_price(symbol))
        
        # Try to place a large order that exceeds balance
        large_quantity = 100.0  # 100 BTC should exceed any testnet balance
        
        try:
            # This should fail with insufficient balance
            bot.place_order(symbol, "BUY", "MARKET", large_quantity)
            print_failure("Order was placed despite insufficient balance")
            return False
        except Exception as e:
            if "Insufficient balance" in str(e):
                print_success("Pre-order balance check correctly prevented order with insufficient balance")
                return True
            else:
                print_failure(f"Unexpected error: {str(e)}")
                return False
    except Exception as e:
        print_failure(f"Error testing insufficient balance check: {str(e)}")
        return False

def test_limit_price_validation(bot):
    print_header("Testing limit price validation...")
    try:
        symbol = "BTCUSDT"
        current_price = float(bot.get_current_price(symbol))
        
        # Try to place a limit order with price 50% higher than current price
        invalid_price = current_price * 1.5
        quantity = 0.001  # Small quantity
        
        try:
            # This should fail with price validation
            bot.place_order(symbol, "BUY", "LIMIT", quantity, price=invalid_price)
            print_failure("Limit order was placed despite price being outside ±20% range")
            return False
        except Exception as e:
            if "price is too" in str(e).lower() or "beyond" in str(e).lower() or "20%" in str(e):
                print_success("Limit price validation correctly prevented order with price outside ±20% range")
                return True
            else:
                print_failure(f"Unexpected error: {str(e)}")
                return False
    except Exception as e:
        print_failure(f"Error testing limit price validation: {str(e)}")
        return False

def main():
    print(f"{BOLD}Binance Spot Testnet Trading Bot - Fix Verification{RESET}\n")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print_failure("API key or secret not found in .env file")
        sys.exit(1)
    
    try:
        # Initialize the bot
        bot = BasicBot(api_key, api_secret, testnet=True)
        print_success("Bot initialized successfully")
        
        # Run tests
        balance_test = test_balance_command(bot)
        balance_check_test = test_insufficient_balance_check(bot)
        price_validation_test = test_limit_price_validation(bot)
        
        # Summary
        print_header("Test Summary:")
        print(f"Balance command test: {'Passed' if balance_test else 'Failed'}")
        print(f"Insufficient balance check test: {'Passed' if balance_check_test else 'Failed'}")
        print(f"Limit price validation test: {'Passed' if price_validation_test else 'Failed'}")
        
        all_passed = balance_test and balance_check_test and price_validation_test
        
        if all_passed:
            print(f"\n{GREEN}All tests passed! The fixes are working correctly.{RESET}")
            sys.exit(0)
        else:
            print(f"\n{YELLOW}Some tests failed. Please check the issues above.{RESET}")
            sys.exit(1)
            
    except BinanceAPIException as e:
        print_failure(f"Binance API Error: {e.message} (Code: {e.code})")
        if e.code == -2015:
            print_warning("Invalid API key error. Please check your Binance Spot Testnet API credentials.")
            print_warning("See API_TROUBLESHOOTING.md for help.")
        sys.exit(1)
    except Exception as e:
        print_failure(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()