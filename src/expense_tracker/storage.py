import csv
from pathlib import Path

from expense_tracker.models import Expense, Income, RecurringExpense, RecurringIncome, Transaction

DATA_FILE = Path("data/transactions.csv")

def save_transactions(transactions: list[Transaction], path: Path = DATA_FILE) -> None:
    """Write all transactions to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "amount", "category", "frequency"])

        for t in transactions:
            type_name = type(t).__name__
            frequency = getattr(t, "frequency", "")
            writer.writerow([type_name, t.amount, t.category, frequency])


def load_transactions(path: Path = DATA_FILE) -> list[Transaction]:
    """Read transactions back from a CSV file. Returns an empty list if the file doesn't exist."""
    if not path.exists():
        return []

    transactions: list[Transaction] = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row["amount"])
            category = row["category"]
            frequency = row["frequency"]
            type_name = row["type"]

            if type_name == "Income":
                transactions.append(Income(amount, category))
            elif type_name == "Expense":
                transactions.append(Expense(amount, category))
            elif type_name == "RecurringIncome":
                transactions.append(RecurringIncome(amount, category, frequency=frequency))
            elif type_name == "RecurringExpense":
                transactions.append(RecurringExpense(amount, category, frequency=frequency))

    return transactions

def add_transaction(
    transactions: list[Transaction],
    amount: float,
    category: str,
    kind: str,
    frequency: str | None = None,
) -> Transaction:
    """Create a transaction of the given kind and append it."""
    if kind == "income":
        transaction = Income(amount, category)
    elif kind == "expense":
        transaction = Expense(amount, category)
    elif kind == "recurring_income":
        transaction = RecurringIncome(amount, category, frequency=frequency or "monthly")
    elif kind == "recurring_expense":
        transaction = RecurringExpense(amount, category, frequency=frequency or "monthly")
    else:
        raise ValueError("Invalid transaction kind.")

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