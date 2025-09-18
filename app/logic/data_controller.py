# app/logic/data_controller.py
from typing import List, Dict, Optional
from ..api.coin_gecko import CoinGeckoAPI
from ..utils.formatting import DataFormatter

class DataController:
    """Orchestrates data flow between the API, data formatting, and UI."""
    
    def __init__(self):
        self.api = CoinGeckoAPI()
        self.formatter = DataFormatter()
        self.current_data: List[Dict] = []
    
    def fetch_top_coins(self, limit: int = 50) -> Optional[List[Dict]]:
        """Fetches and formats top coins data from the API."""
        raw_data = self.api.get_top_coins(limit)
        if raw_data:
            self.current_data = self.formatter.format_coin_data(raw_data)
            return self.current_data
        return None