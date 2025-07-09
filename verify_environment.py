#!/usr/bin/env python3
"""
Environment verification script for Binance Spot Testnet Trading Bot
"""

import os
import sys
import platform
import importlib.util
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def check_mark(success):
    return f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"

def print_header(text):
    print(f"\n{BOLD}{text}{RESET}")

def check_python_version():
    version = sys.version_info
    required_version = (3, 7)
    success = version >= required_version
    print(f"{check_mark(success)} Python version: {platform.python_version()}")
    if not success:
        print(f"  {YELLOW}Required: Python {required_version[0]}.{required_version[1]} or higher{RESET}")
    return success

def check_package(package_name):
    is_installed = importlib.util.find_spec(package_name) is not None
    print(f"{check_mark(is_installed)} {package_name}")
    if not is_installed:
        print(f"  {YELLOW}Missing: Install with 'pip install {package_name}'{RESET}")
    return is_installed

def check_env_file():
    env_path = Path('.env')
    exists = env_path.exists()
    print(f"{check_mark(exists)} .env file")
    
    if exists:
        with open(env_path, 'r') as f:
            content = f.read()
        
        has_api_key = 'BINANCE_API_KEY' in content
        has_api_secret = 'BINANCE_API_SECRET' in content
        
        print(f"  {check_mark(has_api_key)} BINANCE_API_KEY")
        print(f"  {check_mark(has_api_secret)} BINANCE_API_SECRET")
        
        if not has_api_key or not has_api_secret:
            print(f"  {YELLOW}Missing API credentials in .env file{RESET}")
        
        return exists and has_api_key and has_api_secret
    else:
        print(f"  {YELLOW}Create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET{RESET}")
        return False

def check_required_files():
    required_files = ['bot.py', 'main.py']
    all_exist = True
    
    for file in required_files:
        exists = Path(file).exists()
        all_exist = all_exist and exists
        print(f"{check_mark(exists)} {file}")
        
    return all_exist

def main():
    print(f"{BOLD}Binance Spot Testnet Trading Bot - Environment Check{RESET}\n")
    
    print_header("System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    python_ok = check_python_version()
    
    print_header("Required Packages:")
    binance_ok = check_package('binance')
    dotenv_ok = check_package('dotenv')
    
    print_header("Configuration:")
    env_ok = check_env_file()
    
    print_header("Required Files:")
    files_ok = check_required_files()
    
    # Summary
    print_header("Summary:")
    all_ok = python_ok and binance_ok and dotenv_ok and env_ok and files_ok
    
    if all_ok:
        print(f"{GREEN}All checks passed! Your environment is ready.{RESET}")
        print("\nYou can now run the bot with: python main.py")
    else:
        print(f"{YELLOW}Some checks failed. Please fix the issues above before running the bot.{RESET}")
        print("\nFor API connection issues, run: python test_api_connection.py")
        print("For more help, see the API_TROUBLESHOOTING.md file")

if __name__ == "__main__":
    main()