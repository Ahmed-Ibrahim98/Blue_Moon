# app/logic/search_algorithm.py
class SearchAlgorithm:
    """Implements a simple search algorithm for filtering coins by name or symbol."""
    def __init__(self, all_coins: list[dict]):
        self.all_coins = all_coins

    def search(self, query: str) -> list[dict]:
        """Return list of coins matching the search query (case-insensitive)."""
        if not query:
            return self.all_coins

        query = query.lower()
        return [
            coin for coin in self.all_coins
            if query in coin["name"].lower() or query in coin["symbol"].lower()
        ]