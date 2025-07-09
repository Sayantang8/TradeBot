"""
Setup script for Binance Futures Trading Bot
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Binance Futures Testnet API Credentials
# Get these from https://testnet.binancefuture.com
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here

# Optional: Set to True for verbose logging
DEBUG_MODE=False
""")
        print("✅ .env file created. Please update it with your API credentials.")
    else:
        print("✅ .env file already exists.")

def create_log_file():
    """Create log file"""
    if not os.path.exists('bot.log'):
        with open('bot.log', 'w') as f:
            f.write("# Bot Log File\n")
        print("✅ Log file created.")

def main():
    """Main setup function"""
    print("=" * 60)
    print("    BINANCE FUTURES TRADING BOT SETUP")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create .env file
    create_env_file()
    
    # Create log file
    create_log_file()
    
    print("\n" + "=" * 60)
    print("    SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Go to https://testnet.binancefuture.com")
    print("2. Create an account and generate API keys")
    print("3. Update the .env file with your API credentials")
    print("4. Run the bot:")
    print("   - Interactive mode: python main.py")
    print("   - GUI mode: python gui.py")
    print("   - Single command: python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001")
    print("\n⚠️  Remember: This is TESTNET only - no real money involved!")

if __name__ == "__main__":
    main()