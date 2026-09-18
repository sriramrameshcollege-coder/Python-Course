class Expense:
    """Represents a single financial transaction (income or expense)."""

    def __init__(self, amount: float, category: str):
        if amount == 0:
            raise ValueError("Amount cannot be zero.")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty.")

        self.amount = amount
        self.category = category.strip().lower()

    @property
    def is_expense(self) -> bool:
        """True if this transaction is money going out."""
        return self.amount < 0

    def __repr__(self) -> str:
        kind = "Expense" if self.is_expense else "Income"
        return f"{kind}({self.amount}, '{self.category}')"