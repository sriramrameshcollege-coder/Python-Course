from expense_tracker.storage import (
    add_transaction,
    get_total,
    get_totals_by_category,
    parse_amount,
)


def main() -> None:
    print("=== Expense Tracker ===")

    transactions: list[dict] = []

    while True:
        raw_amount = input("Enter amount (or 'q' to quit): ")

        if raw_amount.lower() == "q":
            break

        amount = parse_amount(raw_amount)
        if amount is None:
            print("That's not a valid number, try again.")
            continue

        category = input("Enter category (e.g. food, rent, fun): ")
        add_transaction(transactions, amount, category)

        if amount < 0:
            print(f"Recorded expense: {amount} in {category}")
        else:
            print(f"Recorded income: {amount} in {category}")

    print_summary(transactions)


def print_summary(transactions: list[dict]) -> None:
    print("\n=== Summary ===")

    if not transactions:
        print("No transactions recorded.")
        return

    print(f"Total transactions: {len(transactions)}")
    print(f"Net balance: {get_total(transactions)}")

    print("By category:")
    for category, amount in get_totals_by_category(transactions).items():
        print(f"  {category}: {amount}")


if __name__ == "__main__":
    main()