# Binance Spot Testnet API Troubleshooting Guide

## Error: APIError(code=-2015): Invalid API-key, IP, or permissions for action

### What This Means
This error occurs when the Binance server rejects your API calls due to authentication issues.

### Common Causes and Solutions

| Cause | Solution |
|-------|----------|
| ❌ Wrong base URL | ✅ Must be `https://testnet.binance.vision/api` for Spot Testnet |
| ❌ Invalid API key/secret | ✅ Get new ones from [Binance Testnet](https://testnet.binance.vision) → API Key |
| ❌ IP restriction on API key | ✅ Either disable IP whitelist or whitelist your current IP |
| ❌ Using Futures keys on Spot | ✅ They are not interchangeable — use Spot Testnet keys only |

## How to Fix

### 1. Get New API Keys

1. Go to [Binance Spot Testnet](https://testnet.binance.vision/)
2. Log in (create an account if needed)
3. Click on "Generate HMAC-SHA256 Key"
4. Save both the API Key and Secret Key

### 2. Update Your .env File

Replace your current API credentials in the `.env` file:

```
BINANCE_API_KEY=your_new_spot_testnet_api_key
BINANCE_API_SECRET=your_new_spot_testnet_secret_key
DEBUG_MODE=True
```

### 3. Verify Connection

Run the test script to verify your connection:

```
python test_api_connection.py
```

## Important Notes

- Binance Spot Testnet and Futures Testnet use different API keys
- Testnet accounts are automatically funded with virtual assets
- The Testnet is periodically reset (approximately monthly)
- Only `/api` endpoints are available (not `/sapi`)

## Additional Resources

- [Binance Spot Testnet FAQ](https://testnet.binance.vision/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [Python Binance Library](https://python-binance.readthedocs.io/)

## Still Having Issues?

If you're still experiencing problems after following these steps, check:

1. Network connectivity to Binance servers
2. Firewall or proxy settings that might block API calls
3. Time synchronization on your machine
4. Python-binance package version (should be 1.0.19 or newer)