from expense_tracker.models import Expense, Income, Transaction


def add_transaction(
    transactions: list[Transaction], amount: float, category: str, kind: str
) -> Transaction:
    """Create an Income or Expense (based on `kind`) and append it."""
    if kind == "income":
        transaction = Income(amount, category)
    elif kind == "expense":
        transaction = Expense(amount, category)
    else:
        raise ValueError("kind must be 'income' or 'expense'")

    transactions.append(transaction)
    return transaction


def get_total(transactions: list[Transaction]) -> float:
    """Return the net balance across all transactions."""
    return sum(t.signed_amount for t in transactions)


def get_totals_by_category(transactions: list[Transaction]) -> dict[str, float]:
    """Return a dict mapping category -> summed signed amount."""
    categories: dict[str, float] = {}
    for t in transactions:
        categories[t.category] = categories.get(t.category, 0) + t.signed_amount
    return categories


def filter_by_category(transactions: list[Transaction], category: str) -> list[Transaction]:
    """Return only the transactions matching the given category (case-insensitive)."""
    return [t for t in transactions if t.category.lower() == category.lower()]


def parse_amount(raw_value: str) -> float | None:
    """Try to convert user input into a float. Return None if invalid."""
    try:
        return float(raw_value)
    except ValueError:
        return None