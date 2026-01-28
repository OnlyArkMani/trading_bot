import os
import sys
import click
import logging
from dotenv import load_dotenv

from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError
)

# Load API keys from .env file
load_dotenv()

# Start logging
logger = setup_logging()

def show_order_summary(symbol, side, order_type, quantity, price=None):
    """Show what order we're about to place"""
    click.echo("\n" + "="*50)
    click.echo(click.style("ORDER SUMMARY", fg="cyan", bold=True))
    click.echo("="*50)
    click.echo(f"Symbol:      {symbol}")
    click.echo(f"Side:        {side}")
    click.echo(f"Type:        {order_type}")
    click.echo(f"Quantity:    {quantity}")
    if price:
        click.echo(f"Price:       {price}")
    click.echo("="*50 + "\n")

def show_order_result(response):
    """Show the result after placing order"""
    click.echo("\n" + "="*50)
    click.echo(click.style("ORDER RESULT", fg="green", bold=True))
    click.echo("="*50)
    click.echo(f"Order ID:       {response.get('orderId', 'N/A')}")
    click.echo(f"Status:         {response.get('status', 'N/A')}")
    click.echo(f"Symbol:         {response.get('symbol', 'N/A')}")
    click.echo(f"Side:           {response.get('side', 'N/A')}")
    click.echo(f"Quantity:       {response.get('origQty', 'N/A')}")
    click.echo(f"Executed Qty:   {response.get('executedQty', 'N/A')}")
    
    if 'avgPrice' in response and response['avgPrice'] != '0':
        click.echo(f"Avg Price:      {response.get('avgPrice', 'N/A')}")
    
    click.echo("="*50 + "\n")

@click.command()
@click.option('--symbol', '-s', required=True, help='Trading symbol like BTCUSDT')
@click.option('--side', '-d', required=True, type=click.Choice(['BUY', 'SELL', 'buy', 'sell'], case_sensitive=False), help='BUY or SELL')
@click.option('--type', '-t', 'order_type', required=True, type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit'], case_sensitive=False), help='MARKET or LIMIT')
@click.option('--quantity', '-q', required=True, type=float, help='How much to trade')
@click.option('--price', '-p', type=float, default=None, help='Price for limit orders')
def place_order(symbol, side, order_type, quantity, price):
    """
    Place an order on Binance Futures Testnet
    
    Examples:
    
    Market order:
        python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
    
    Limit order:
        python cli.py -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 45000
    """
    try:
        # Get API keys
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            click.echo(click.style("Error: Can't find API keys!", fg="red"))
            click.echo("Make sure you have a .env file with your keys")
            logger.error("API keys not found")
            sys.exit(1)
        
        # Validate everything
        logger.info("Checking inputs...")
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)
        
        # Show what we're doing
        show_order_summary(symbol, side, order_type, quantity, price)
        
        # Set up the client and order manager
        client = BinanceClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        # Place the order
        click.echo(click.style("Placing order...", fg="yellow"))
        response = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        # Show the result
        show_order_result(response)
        
        # Success!
        click.echo(click.style("✓ Order placed successfully!", fg="green", bold=True))
        logger.info(f"Order placed: ID {response.get('orderId')}")
        
    except ValidationError as e:
        click.echo(click.style(f"Validation Error: {str(e)}", fg="red"))
        logger.error(f"Validation failed: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"))
        logger.exception("Something went wrong")
        sys.exit(1)

if __name__ == '__main__':
    place_order()