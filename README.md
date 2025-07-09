# Binance Spot Testnet Trading Bot

A command-line trading bot for Binance Spot Testnet that allows you to place market and limit orders, view your holdings, check balances, and manage orders. Features pre-order balance validation and limit price checks for safer trading.

## Setup Instructions

### 1. Environment Setup
- Ensure Python 3.7 or higher is installed
- Create and activate a virtual environment (recommended):
  ```bash
  python -m venv .venv
  # On Windows:
  .venv\Scripts\activate
  # On Unix/MacOS:
  source .venv/bin/activate
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
This will install:
- `python-binance`: For Binance API interactions
- `python-dotenv`: For environment variable management
- Additional development and testing packages

### 3. Get Binance Spot Testnet API Keys
1. Visit [Binance Spot Testnet](https://testnet.binance.vision/)
2. Log in with your Binance account or GitHub
3. Click "Generate HMAC-SHA256 Key"
4. Save both the API Key and Secret Key

### 4. Configure Environment
1. Create a `.env` file in the project root:
   ```bash
   BINANCE_API_KEY=your_spot_testnet_api_key
   BINANCE_API_SECRET=your_spot_testnet_secret_key
   DEBUG_MODE=True  # Set to False in production
   ```

### 5. Verify Setup
Run the environment verification script:
```bash
python verify_environment.py
```
This will check:
- Python version
- Required packages
- Configuration files
- Environment setup

## Usage

### Interactive Mode

Start the bot in interactive mode:
```bash
python main.py
```

This launches the CLI interface with the following commands:

| Command   | Description                                    | Example Usage |
|-----------|------------------------------------------------|---------------|
| `help`    | Show available commands and usage              | `help` |
| `place`   | Place a new order (market/limit/stop)          | `place` |
| `balance` | Show all non-zero account balances             | `balance` |
| `holdings`| Display current asset holdings                 | `holdings` |
| `orders`  | List all open orders                          | `orders` |
| `cancel`  | Cancel an open order by ID                     | `cancel` |
| `price`   | Get current price for a trading pair           | `price BTCUSDT` |
| `exit`    | Exit the program                              | `exit` |

### Single Command Mode

Execute a single command without entering interactive mode:
```bash
python main.py <command> [arguments]
```

Examples:
```bash
# Check BTCUSDT price
python main.py price BTCUSDT

# View account balance
python main.py balance

# Show current holdings
python main.py holdings
```

### Testing the Bot

To verify your setup and API connection:

```bash
python test_api_connection.py  # Test API connectivity
python verify_environment.py   # Verify environment setup
python verify_fixes.py         # Test trading functionality
```

These scripts will help diagnose any issues with your setup.

## Features

- 📊 View account balances and non-zero holdings
- 💰 Place market, limit, and stop orders with safety checks
- 🔍 Check current market prices in real-time
- ❌ Cancel open orders with order ID
- 📋 List all active orders
- 🛡️ Pre-order balance validation
- 💱 Limit price validation (±20% of market price)
- 🔄 Interactive command-line interface
- 🔍 Comprehensive error handling and diagnostics

## Important Notes

### Testnet Environment
- This bot operates on Binance Spot Testnet, not the real Binance exchange
- Uses virtual funds - no real cryptocurrency or money is involved
- Testnet is reset periodically (approximately monthly)
- All balances and orders are cleared during resets

### API Considerations
- Spot Testnet API keys are different from Futures Testnet
- API keys may expire or be invalidated during Testnet resets
- Base URL for Spot Testnet: `https://testnet.binance.vision/api`
- Rate limits are more relaxed than production

### Safety Features
- Pre-order balance validation prevents insufficient balance errors
- Limit orders are restricted to ±20% of current market price
- All operations are logged for debugging
- Comprehensive error messages with troubleshooting guidance

### Best Practices
- Always test new strategies with small amounts first
- Monitor the bot's operation during initial setup
- Keep your API keys secure and never share them
- Check `API_TROUBLESHOOTING.md` if you encounter issues

## Command Reference

### Available Commands

#### Account Information
- `balance`
  - Shows all non-zero balances in your account
  - Displays both free and locked amounts
  - Example: `balance`

- `holdings`
  - Lists current asset holdings
  - Shows total balance (free + locked)
  - Example: `holdings`

#### Trading Operations
- `place`
  - Interactive order placement
  - Supports market, limit, and stop orders
  - Includes balance and price validations
  - Example: `place`

- `orders`
  - Lists all open orders
  - Shows order ID, symbol, type, side, and status
  - Example: `orders`

- `cancel`
  - Cancels an open order by order ID
  - Example: `cancel`

#### Market Information
- `price`
  - Gets current price for a trading pair
  - Example: `price BTCUSDT`

#### System Commands
- `help`
  - Shows detailed help message
  - Lists all available commands
  - Example: `help`

- `exit`
  - Safely exits the program
  - Example: `exit`

### Command Format
```
python main.py [command] [arguments]
```

### Interactive Mode Banner
```
╔════════════════════════════════════════════════════════════╗
║                 BINANCE SPOT TESTNET TRADER                 ║
╚════════════════════════════════════════════════════════════╝
```

## Error Handling & Safety Features

The bot implements multiple safety checks and validations:

### Pre-Order Validations
- Balance check before order placement
- Limit price validation (±20% of current market price)
- Symbol pair validation

### Error Handling
- Detailed error messages with suggestions
- API connection error diagnostics
- Invalid input protection

## Diagnostic & Debugging

### Diagnostic Tools

1. **API Connection Tester**
   ```bash
   python test_api_connection.py
   ```
   - Verifies API key validity
   - Tests server connectivity
   - Checks account permissions

2. **Environment Checker**
   ```bash
   python verify_environment.py
   ```
   - Validates Python version
   - Checks required packages
   - Verifies configuration files

3. **Trading Function Verifier**
   ```bash
   python verify_fixes.py
   ```
   - Tests balance reporting
   - Validates order placement
   - Checks safety features

### Logging

The bot maintains detailed logs in `bot.log` for debugging:

- **Log Levels**
  - `INFO`: Normal operations
  - `WARNING`: Potential issues
  - `ERROR`: Operation failures
  - `DEBUG`: Detailed debugging (when DEBUG_MODE=True)

- **Log Format**
  ```
  YYYY-MM-DD HH:MM:SS,ms | LEVEL | Message
  ```

- **Key Events Logged**
  - Order placements and results
  - Balance checks
  - API calls and responses
  - Error conditions and stack traces

### Troubleshooting

1. **Common Issues**
   - API connection errors
   - Insufficient balance errors
   - Invalid price range errors
   - Order placement failures

2. **Debug Mode**
   - Set `DEBUG_MODE=True` in `.env` for verbose logging
   - Helps identify API call issues
   - Shows detailed error traces

For detailed troubleshooting steps and solutions to common issues, refer to the `API_TROUBLESHOOTING.md` guide.

### LICENSE
  - This project is licensed under the MIT License. For more details, please see the `LICENSE` file included in this repository.
