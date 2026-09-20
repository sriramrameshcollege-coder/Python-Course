import numpy as np

from expense_tracker.models import Transaction


def get_amounts_array(transactions: list[Transaction]) -> np.ndarray:
    """Convert signed amounts into a numpy array for numeric analysis."""
    return np.array([t.signed_amount for t in transactions])


def get_stats(transactions: list[Transaction]) -> dict[str, float]:
    """Return basic descriptive statistics over all signed amounts."""
    amounts = get_amounts_array(transactions)

    if amounts.size == 0:
        return {"mean": 0.0, "std": 0.0, "biggest_income": 0.0, "biggest_expense": 0.0}

    positive = amounts[amounts > 0]
    negative = amounts[amounts < 0]

    return {
        "mean": float(np.mean(amounts)),
        "std": float(np.std(amounts)),
        "biggest_income": float(np.max(positive)) if positive.size > 0 else 0.0,
        "biggest_expense": float(np.min(negative)) if negative.size > 0 else 0.0,
    }


def get_running_balance(transactions: list[Transaction]) -> np.ndarray:
    """Return the cumulative balance after each transaction, in order."""
    amounts = get_amounts_array(transactions)
    return np.cumsum(amounts)