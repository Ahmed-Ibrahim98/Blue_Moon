# app/logic/search_algorithm.py
class SearchAlgorithm:
    def __init__(self, all_coins: list[dict]):
        self.all_coins = all_coins

    def search(self, query: str) -> list[dict]:
        if not query:
            return self.all_coins

        query = query.lower()
        return [
            coin for coin in self.all_coins
            if query in coin["name"].lower() or query in coin["symbol"].lower()
        ]