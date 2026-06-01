import hashlib
import hmac
import time
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceClient:
    """
    Wrapper for Binance Futures Testnet API.
    Handles authentication and API requests.
    """
    
    def __init__(self, api_key, api_secret, base_url='https://testnet.binancefuture.com'):
        """
        Initialize Binance client.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            base_url (str): Base URL for API requests
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key
        })
        logger.info(f"Initialized Binance client with base URL: {base_url}")
    
    def _generate_signature(self, params):
        """
        Generate HMAC SHA256 signature for API request.
        
        Args:
            params (dict): Request parameters
        
        Returns:
            str: Generated signature
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method, endpoint, params=None, signed=False):
        """
        Make an API request to Binance.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict): Request parameters
            signed (bool): Whether request requires signature
        
        Returns:
            dict: API response
        
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        # Log request details (omit signature for security)
        safe_params = {k: v for k, v in params.items() if k != 'signature'}
        logger.info(f"Making {method} request to {endpoint} | params: {safe_params}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, params=params)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Response [{response.status_code}]: {data}")
            
            return data
        
        except requests.exceptions.HTTPError as e:
            error_body = e.response.text if e.response else "No response body"
            logger.error(f"HTTP error {e.response.status_code if e.response else 'unknown'}: {error_body}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network connection failed: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get_account_info(self):
        """
        Get account information.
        
        Returns:
            dict: Account information
        """
        logger.info("Fetching account information")
        return self._make_request('GET', '/fapi/v2/account', signed=True)
    
    def get_exchange_info(self, symbol=None):
        """
        Get exchange information for symbol.
        
        Args:
            symbol (str): Trading symbol
        
        Returns:
            dict: Exchange information
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        logger.info(f"Fetching exchange info for {symbol if symbol else 'all symbols'}")
        return self._make_request('GET', '/fapi/v1/exchangeInfo', params=params)
    
    def get_ticker_price(self, symbol):
        """
        Get current ticker price for symbol.
        
        Args:
            symbol (str): Trading symbol
        
        Returns:
            dict: Ticker price information
        """
        logger.info(f"Fetching ticker price for {symbol}")
        return self._make_request('GET', '/fapi/v1/ticker/price', params={'symbol': symbol})
