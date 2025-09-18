# app/utils/formatting.py
from typing import List, Dict, Any

class DataFormatter:
    """A utility class for formatting cryptocurrency data."""
    
    @staticmethod
    def format_coin_data(raw_coins: List[Dict]) -> List[Dict[str, Any]]:
        """Formats raw API data into a structured list of dictionaries."""
        return [
            {
                "rank": coin.get('market_cap_rank', 0),
                "name": coin.get('name', 'N/A'),
                "symbol": coin.get('symbol', '').upper(),
                "price": coin.get('current_price', 0.0),
                "change_24h": coin.get('price_change_percentage_24h', 0.0),
                "market_cap": coin.get('market_cap', 0)
            }
            for coin in raw_coins
        ]

    @staticmethod
    def format_currency(value: float) -> str:
        if not isinstance(value, (int, float)) or value <= 0:
            return "N/A"
        
        if value >= 1_000_000_000_000:
            return f"${value/1_000_000_000_000:,.2f} T"
        if value >= 1_000_000_000:
            return f"${value/1_000_000_000:,.2f} B"
        if value >= 1_000_000:
            return f"${value/1_000_000:,.2f} M"
        return f"${value:,.2f}"

    @staticmethod
    def format_price(price: float) -> str:
        if not isinstance(price, (int, float)) or price <= 0:
            return "N/A"
        
        if price >= 1.0:
            return f"${price:,.2f}"
        if price < 0.000001:
            return f"${price:,.8f}" # Show more precision for very small values
        return f"${price:,.6f}"

    @staticmethod
    def format_percentage_change(change: float) -> str:
        if change is None:
            return "N/A"
        return f"{change:+.2f}%"