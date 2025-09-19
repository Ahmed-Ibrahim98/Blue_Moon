# app/utils/file_saver.py
import csv
from typing import List, Dict
from app.utils.formatting import DataFormatter

class FileSaver:
    @staticmethod
    def save_csv(file_path: str, data: List[Dict], raw: bool = False) -> bool:
        """Save list of coins (dicts) to CSV. Formatted or raw values depending on `raw`."""
        if not data:
            return False

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = ["Rank", "Name (Symbol)", "Price", "24h %", "Market Cap"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for coin in data:
                    if raw:
                        # Plain values for machine use
                        formatted_coin = {
                            "Rank": coin.get("rank"),
                            "Name (Symbol)": f"{coin.get('name')} ({coin.get('symbol')})",
                            "Price": coin.get("price"),
                            "24h %": coin.get("change_24h"),
                            "Market Cap": coin.get("market_cap"),
                        }
                    else:
                        # Human-friendly formatting
                        formatted_coin = {
                            "Rank": coin.get("rank"),
                            "Name (Symbol)": f"{coin.get('name')} ({coin.get('symbol')})",
                            "Price": DataFormatter.format_price(coin["price"]),
                            "24h %": DataFormatter.format_percentage_change(coin["change_24h"]),
                            "Market Cap": DataFormatter.format_currency(coin["market_cap"]),
                        }
                    writer.writerow(formatted_coin)

            return True
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return False
