# Binance Futures Trading Bot

A simple Python script to place orders on Binance Futures Testnet. I built this as part of a job application task.

## What it does

- Places market orders (buy/sell at current price)
- Places limit orders (buy/sell at a specific price)
- Logs everything to a file
- Validates inputs before sending to API
- Shows order confirmation after placing

## Project Structure

```
trading_bot/
├── bot/
│   ├── client.py         # Handles API calls to Binance
│   ├── orders.py         # Logic for placing orders
│   ├── validators.py     # Checks if inputs are valid
│   └── logging_config.py # Sets up logging
├── cli.py                # Main script you run
├── requirements.txt      # Libraries needed
└── README.md            # This file
```

## How to Set It Up

### Step 1: Get API Keys

1. Go to https://testnet.binancefuture.com
2. Sign up with your email
3. Go to API Management and create new API key
4. Copy both the API Key and Secret Key somewhere safe

### Step 2: Install Python Packages

```bash
# Go to the project folder
cd trading_bot

# Install what's needed
pip install -r requirements.txt
```

### Step 3: Add Your API Keys

Create a file called `.env` in the main folder:

```
BINANCE_API_KEY=paste_your_key_here
BINANCE_API_SECRET=paste_your_secret_here
```

Note: Don't upload this .env file anywhere public!

## How to Use

### Basic format:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Options you can use:
- `--symbol` or `-s`: Which coin (like BTCUSDT, ETHUSDT)
- `--side` or `-d`: BUY or SELL
- `--type` or `-t`: MARKET or LIMIT
- `--quantity` or `-q`: How much to buy/sell
- `--price` or `-p`: Price for limit orders (not needed for market orders)

### Examples:

Buy Bitcoin at market price:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Sell Bitcoin at a specific price:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 45000
```

Shorter version using flags:
```bash
python cli.py -s ETHUSDT -d BUY -t MARKET -q 0.01
```

## What You'll See

When you run a command, you'll see:

1. A summary of your order
2. "Placing order..." message
3. Results from Binance with order ID and status
4. Success or error message

Example:
```
==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol:      BTCUSDT
Side:        BUY
Type:        MARKET
Quantity:    0.001
==================================================

Placing order...

==================================================
ORDER RESPONSE
==================================================
Order ID:       12345678
Status:         FILLED
Symbol:         BTCUSDT
Quantity:       0.001
Executed Qty:   0.001
Avg Price:      43250.50
==================================================

✓ Order placed successfully!
```

## Logging

Everything gets saved to log files in the `logs/` folder. Each time you run the bot, it creates a new log file with a timestamp.

The logs show:
- What you tried to do
- What the API said back
- Any errors that happened

## Common Errors and Fixes

**"API credentials not found"**
- Make sure you created the .env file
- Check that you pasted your keys correctly

**"Symbol must end with USDT"**
- Use symbols like BTCUSDT, ETHUSDT (not just BTC or ETH)

**"Price is required for LIMIT orders"**
- Add --price when using --type LIMIT

**API errors**
- Check your API keys are correct
- Make sure your testnet account has test money

## Testing Tips

Before using real money (don't use this for real trading though, it's just for testnet):

1. Use small amounts like 0.001
2. Try both market and limit orders
3. Try buying and selling
4. Check the Binance testnet website to confirm orders went through
5. Look at the log files if something goes wrong

## Things I Assumed

- This only works on testnet (not real trading)
- Only works with USDT futures (not other types)
- Limit orders use GTC (Good Till Cancel) 
- You have Python 3 installed
- You have internet connection

## If Something Breaks

- Check the log files in logs/ folder
- Make sure your .env file exists and has the right keys
- Try running the command again
- Make sure you typed the symbol correctly (BTCUSDT not btcusdt)

## Notes

- This is for learning and testing only
- Never share your API keys with anyone
- The .env file should not be uploaded to GitHub
- Test everything on testnet first

## Future Ideas

Things I might add later:
- Stop loss orders
- Ability to cancel orders
- Check account balance
- See open positions
- Better error messages