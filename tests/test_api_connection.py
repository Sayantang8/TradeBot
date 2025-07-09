#!/usr/bin/env python3
"""
Simple test script to verify Binance Spot Testnet API connection
"""

import os
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
BASE_URL = "https://testnet.binance.vision/api"

print("\n===== Binance Spot Testnet API Connection Test =====")
print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:] if API_KEY else 'None'}")
print(f"Base URL: {BASE_URL}")

try:
    # Initialize the client
    print("\nInitializing Binance client...")
    client = Client(API_KEY, API_SECRET, testnet=True)
    client.API_URL = BASE_URL
    
    # Test server connection
    print("Testing server connection...")
    server_time = client.get_server_time()
    print(f"Server time: {server_time['serverTime']}")
    
    # Test account access
    print("\nTesting account access...")
    account_info = client.get_account()
    print("✅ SUCCESS: Account access verified!")
    
    # Print account details
    print("\n===== Account Details =====")
    print(f"Account status: {account_info['accountType']}")
    print(f"Can trade: {account_info['canTrade']}")
    print(f"Can withdraw: {account_info['canWithdraw']}")
    print(f"Can deposit: {account_info['canDeposit']}")
    
    # Print balances with non-zero amounts
    print("\n===== Account Balances =====")
    balances = [b for b in account_info['balances'] if float(b['free']) > 0 or float(b['locked']) > 0]
    
    if balances:
        for balance in balances:
            print(f"{balance['asset']}: Free={balance['free']}, Locked={balance['locked']}")
    else:
        print("No assets with balance found.")
    
    print("\n✅ All tests passed! Your API connection is working correctly.")
    sys.exit(0)
    
except BinanceAPIException as e:
    print(f"\n❌ API ERROR: {e.message} (Code: {e.code})")
    
    # Provide specific guidance based on error code
    if e.code == -2015:
        print("\n🔍 TROUBLESHOOTING STEPS:")
        print("1. Verify your API key and secret are correct")
        print("2. Make sure you're using Spot Testnet keys (not Futures Testnet)")
        print("3. Check if your API key has IP restrictions")
        print("4. Get new API keys from: https://testnet.binance.vision")
    
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n🔍 TROUBLESHOOTING STEPS:")
    print("1. Check your internet connection")
    print("2. Verify the Binance Testnet is operational")
    print("3. Make sure python-binance package is installed (pip install python-binance)")
    sys.exit(1)