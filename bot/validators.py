import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_symbol(symbol):
    """
    Validate trading symbol format.
    
    Args:
        symbol (str): Trading pair symbol (e.g., BTCUSDT)
    
    Returns:
        str: Uppercase symbol
    
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    symbol = symbol.upper()
    
    if not symbol.endswith('USDT'):
        raise ValidationError("Symbol must end with USDT for USDT-M futures")
    
    logger.info(f"Validated symbol: {symbol}")
    return symbol

def validate_side(side):
    """
    Validate order side (BUY/SELL).
    
    Args:
        side (str): Order side
    
    Returns:
        str: Uppercase side
    
    Raises:
        ValidationError: If side is invalid
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Side must be a non-empty string")
    
    side = side.upper()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError("Side must be either BUY or SELL")
    
    logger.info(f"Validated side: {side}")
    return side

def validate_order_type(order_type):
    """
    Validate order type (MARKET/LIMIT).
    
    Args:
        order_type (str): Order type
    
    Returns:
        str: Uppercase order type
    
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type must be a non-empty string")
    
    order_type = order_type.upper()
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError("Order type must be either MARKET or LIMIT")
    
    logger.info(f"Validated order type: {order_type}")
    return order_type

def validate_quantity(quantity):
    """
    Validate order quantity.
    
    Args:
        quantity (float): Order quantity
    
    Returns:
        float: Validated quantity
    
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a valid number")
    
    if qty <= 0:
        raise ValidationError("Quantity must be greater than 0")
    
    logger.info(f"Validated quantity: {qty}")
    return qty

def validate_price(price, order_type):
    """
    Validate order price (required for LIMIT orders).
    
    Args:
        price (float): Order price
        order_type (str): Order type
    
    Returns:
        float or None: Validated price
    
    Raises:
        ValidationError: If price is invalid
    """
    if order_type == 'LIMIT':
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        
        try:
            p = float(price)
        except (ValueError, TypeError):
            raise ValidationError("Price must be a valid number")
        
        if p <= 0:
            raise ValidationError("Price must be greater than 0")
        
        logger.info(f"Validated price: {p}")
        return p
    
    return None