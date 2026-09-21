import numpy as np
import pandas as pd
from pathlib import Path
from expense_tracker.models import Transaction


def get_amounts_array(transactions: list[Transaction]) -> np.ndarray:
    """Convert signed amounts into a numpy array for numeric analysis."""
    return np.array([t.signed_amount for t in transactions])


def get_stats(transactions: list[Transaction]) -> dict[str, float]:
    """Return separate descriptive statistics for income and expenses."""
    amounts = get_amounts_array(transactions)

    if amounts.size == 0:
        return {
            "income_mean": 0.0, "income_std": 0.0,
            "expense_mean": 0.0, "expense_std": 0.0,
            "biggest_income": 0.0, "biggest_expense": 0.0,
        }

    income_amounts = amounts[amounts > 0]
    expense_amounts = amounts[amounts < 0]

    return {
        "income_mean": float(np.mean(income_amounts)) if income_amounts.size > 0 else 0.0,
        "income_std": float(np.std(income_amounts)) if income_amounts.size > 0 else 0.0,
        "expense_mean": float(np.mean(expense_amounts)) if expense_amounts.size > 0 else 0.0,
        "expense_std": float(np.std(expense_amounts)) if expense_amounts.size > 0 else 0.0,
        "biggest_income": float(np.max(income_amounts)) if income_amounts.size > 0 else 0.0,
        "biggest_expense": float(np.min(expense_amounts)) if expense_amounts.size > 0 else 0.0,
    }


def get_running_balance(transactions: list[Transaction]) -> np.ndarray:
    """Return the cumulative balance after each transaction, in order."""
    amounts = get_amounts_array(transactions)
    return np.cumsum(amounts)

def get_biggest_expense_category(transactions: list[Transaction]) -> tuple[str, float] | None:
    """Return the (category, total) with the largest total expense amount."""
    from expense_tracker.storage import get_totals_by_category

    totals = get_totals_by_category(transactions)
    expense_totals = {cat: amt for cat, amt in totals.items() if amt < 0}

    if not expense_totals:
        return None

    categories = np.array(list(expense_totals.keys()))
    amounts = np.array(list(expense_totals.values()))

    idx = np.argmin(amounts)  # most negative = biggest expense
    return str(categories[idx]), float(amounts[idx])

def load_as_dataframe(path: Path = Path("data/transactions.csv")) -> pd.DataFrame:
    """Load the transactions CSV into a pandas DataFrame."""
    if not path.exists():
        return pd.DataFrame(columns=["type", "amount", "category", "frequency"])

    df = pd.read_csv(path)

    # Recreate signed_amount: negative for Expense/RecurringExpense, positive otherwise
    df["signed_amount"] = df.apply(
        lambda row: -row["amount"] if "Expense" in row["type"] else row["amount"],
        axis=1,
    )
    return df


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return total signed amount per category, sorted descending."""
    return (
        df.groupby("category")["signed_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_monthly_summary(df: pd.DataFrame) -> pd.Series:
    """Return count of transactions per type (Income/Expense/Recurring*)."""
    return df["type"].value_counts()