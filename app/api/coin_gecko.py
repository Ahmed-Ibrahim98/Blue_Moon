# app/api/coin_gecko.py
import requests
import time
from typing import List, Dict, Optional
from ..config import API_BASE_URL, API_TIMEOUT

class CoinGeckoAPI:
    """A client for interacting with the CoinGecko API."""
    
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.2 # ~50 requests/min limit

    def _rate_limit(self):
        """Ensures requests do not exceed the API rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def get_top_coins(self, limit: int = 50, currency: str = 'usd') -> Optional[List[Dict]]:
        """Fetches the top N cryptocurrencies by market cap."""
        self._rate_limit()
        
        endpoint = "/coins/markets"
        params = {
            'vs_currency': currency,
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': 'false'
        }
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=self.timeout)
            response.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error fetching top coins: {e}")
            return None