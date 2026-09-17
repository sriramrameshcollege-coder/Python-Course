def add_transaction(transactions: list[dict], amount: float, category: str) -> dict:
    """Create a transaction dict and append it to the transactions list."""
    transaction = {"amount": amount, "category": category}
    transactions.append(transaction)
    return transaction


def get_total(transactions: list[dict]) -> float:
    """Return the net balance across all transactions."""
    return sum(t["amount"] for t in transactions)


def get_totals_by_category(transactions: list[dict]) -> dict[str, float]:
    """Return a dict mapping category -> summed amount."""
    categories: dict[str, float] = {}
    for t in transactions:
        categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]
    return categories


def parse_amount(raw_value: str) -> float | None:
    """Try to convert user input into a float. Return None if invalid."""
    try:
        return float(raw_value)
    except ValueError:
        return None


def filter_by_category(transactions: list[dict], category: str) -> list[dict]:
    """Return only the transactions matching the given category (case-insensitive)."""
    return [t for t in transactions if t["category"].lower() == category.lower()]