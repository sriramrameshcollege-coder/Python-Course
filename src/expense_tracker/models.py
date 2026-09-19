class Transaction:
    """Base class for any financial transaction. Always stores a positive amount."""

    def __init__(self, amount: float, category: str):
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty.")

        self.amount = amount
        self.category = category.strip().lower()

    @property
    def signed_amount(self) -> float:
        """Amount as it should count toward the balance. Overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement signed_amount.")

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.amount}, '{self.category}')"


class Income(Transaction):
    """Money coming in. Counts positively toward the balance."""

    @property
    def signed_amount(self) -> float:
        return self.amount


class Expense(Transaction):
    """Money going out. Counts negatively toward the balance."""

    @property
    def signed_amount(self) -> float:
        return -self.amount


class Recurring:
    """Mixin that adds a frequency label to any transaction. Not used standalone."""

    def __init__(self, *args, frequency: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.frequency = frequency.strip().lower()

    def __repr__(self) -> str:
        base = super().__repr__()
        return f"{base} [recurring: {self.frequency}]"


class RecurringIncome(Recurring, Income):
    """Income that repeats on a schedule, e.g. salary."""
    pass


class RecurringExpense(Recurring, Expense):
    """An expense that repeats on a schedule, e.g. rent or a subscription."""
    pass