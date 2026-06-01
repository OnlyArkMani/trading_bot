import logging
from bot.client import BinanceClient

logger = logging.getLogger(__name__)

class OrderManager:
    """
    Manages order placement on Binance Futures.
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize OrderManager.
        
        Args:
            client (BinanceClient): Binance API client
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order.
        
        Args:
            symbol (str): Trading symbol
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
        
        Returns:
            dict: Order response
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        }
        
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        return self.client._make_request('POST', '/fapi/v1/order', params=params, signed=True)
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order.
        
        Args:
            symbol (str): Trading symbol
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
            price (float): Limit price
        
        Returns:
            dict: Order response
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'quantity': quantity,
            'price': price,
            'timeInForce': 'GTC'  # Good Till Cancel
        }
        
        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
        return self.client._make_request('POST', '/fapi/v1/order', params=params, signed=True)
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order based on type.
        
        Args:
            symbol (str): Trading symbol
            side (str): Order side (BUY/SELL)
            order_type (str): Order type (MARKET/LIMIT)
            quantity (float): Order quantity
            price (float, optional): Limit price
        
        Returns:
            dict: Order response
        
        Raises:
            ValueError: If order type is invalid or required parameters missing
        """
        if order_type == 'MARKET':
            return self.place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            return self.place_limit_order(symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
    
    def get_order_status(self, symbol, order_id):
        """
        Get status of an order.
        
        Args:
            symbol (str): Trading symbol
            order_id (int): Order ID
        
        Returns:
            dict: Order status
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Fetching order status for order {order_id}")
        return self.client._make_request('GET', '/fapi/v1/order', params=params, signed=True)
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel an order.
        
        Args:
            symbol (str): Trading symbol
            order_id (int): Order ID
        
        Returns:
            dict: Cancellation response
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Canceling order {order_id}")
        return self.client._make_request('DELETE', '/fapi/v1/order', params=params, signed=True)
