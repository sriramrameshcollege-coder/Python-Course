from expense_tracker.models import Transaction
from expense_tracker.storage import (
    add_transaction,
    filter_by_category,
    get_total,
    get_totals_by_category,
    parse_amount,
)


def main() -> None:
    print("=== Expense Tracker ===")

    transactions: list[Transaction] = []

    while True:
        kind = input("Income or expense? (i/e, or 'q' to quit): ").strip().lower()

        if kind == "q":
            break
        if kind not in ("i", "e"):
            print("Please enter 'i', 'e', or 'q'.")
            continue

        raw_amount = input("Enter amount (positive number): ")
        amount = parse_amount(raw_amount)
        if amount is None:
            print("That's not a valid number, try again.")
            continue

        category = input("Enter category (e.g. food, rent, fun): ")

        try:
            transaction = add_transaction(
                transactions, amount, category, "income" if kind == "i" else "expense"
            )
        except ValueError as e:
            print(f"Invalid entry: {e}")
            continue

        print(f"Recorded {transaction}")

    print_summary(transactions)


def print_summary(transactions: list[Transaction]) -> None:
    print("\n=== Summary ===")

    if not transactions:
        print("No transactions recorded.")
        return

    print(f"Total transactions: {len(transactions)}")
    print(f"Net balance: {get_total(transactions)}")

    print("By category:")
    for category, amount in get_totals_by_category(transactions).items():
        print(f"  {category}: {amount}")

    lookup = input("\nWant to see transactions for a specific category? (enter category or press Enter to skip): ")
    if lookup:
        matches = filter_by_category(transactions, lookup)
        if matches:
            print(f"\nTransactions in '{lookup}':")
            for t in matches:
                print(f"  {t}")
        else:
            print(f"No transactions found for '{lookup}'.")


if __name__ == "__main__":
    main()