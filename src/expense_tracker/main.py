from expense_tracker.models import Transaction
from expense_tracker.viz import (
    build_category_chart,
    build_income_vs_expense_chart,
    build_running_balance_chart,
    save_chart,
    maybe_show,
)
from expense_tracker.analysis import get_biggest_expense_category, get_running_balance, get_stats, get_category_summary, get_monthly_summary, load_as_dataframe
from expense_tracker.storage import (
    add_transaction,
    filter_by_category,
    get_total,
    get_totals_by_category,
    load_transactions,
    parse_amount,
    save_transactions,
)

def main() -> None:
    print("=== Expense Tracker ===")

    transactions: list[Transaction] = load_transactions()
    print(f"Loaded {len(transactions)} existing transactions.")

    while True:
        kind = input("Income, expense, or recurring? (i/e/r, or 'q' to quit): ").strip().lower()

        if kind == "q":
            break
        if kind not in ("i", "e", "r"):
            print("Please enter 'i', 'e', 'r', or 'q'.")
            continue

        raw_amount = input("Enter amount (positive number): ")
        amount = parse_amount(raw_amount)
        if amount is None:
            print("That's not a valid number, try again.")
            continue

        category = input("Enter category (e.g. food, rent, fun): ")

        frequency = None
        if kind == "r":
            direction = input("Is this recurring income or expense? (i/e): ").strip().lower()
            frequency = input("Frequency (e.g. monthly, weekly): ")
            resolved_kind = "recurring_income" if direction == "i" else "recurring_expense"
        else:
            resolved_kind = "income" if kind == "i" else "expense"

        try:
            transaction = add_transaction(transactions, amount, category, resolved_kind, frequency)
        except ValueError as e:
            print(f"Invalid entry: {e}")
            continue

        print(f"Recorded {transaction}")

    save_transactions(transactions)
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

    stats = get_stats(transactions)
    print("\n=== Numpy Stats ===")
    print(f"Average income: {stats['income_mean']:.2f} (std: {stats['income_std']:.2f})")
    print(f"Average expense: {stats['expense_mean']:.2f} (std: {stats['expense_std']:.2f})")
    print(f"Biggest income: {stats['biggest_income']:.2f}")
    print(f"Biggest expense: {stats['biggest_expense']:.2f}")

    running = get_running_balance(transactions)
    print(f"Running balance over time: {running.tolist()}")

    biggest = get_biggest_expense_category(transactions)
    if biggest:
        category, amount = biggest
        print(f"Category with biggest expense: {category} ({amount:.2f})")    

    while True:
        lookup = input("\nWant to see transactions for a specific category? (enter category or press Enter to skip): ")
        if not lookup:
            break

        matches = filter_by_category(transactions, lookup)
        if matches:
            print(f"\nTransactions in '{lookup}':")
            for t in matches:
                print(f"  {t}")
        else:
            print(f"No transactions found for '{lookup}'.")

    print("\n=== Pandas Analysis ===")
    df = load_as_dataframe()
    if not df.empty:
        print("\nCategory totals (sorted):")
        print(get_category_summary(df).to_string(index=False))

        print("\nTransaction type counts:")
        print(get_monthly_summary(df).to_string())

        if not df.empty:
            view_charts = input("\nWant to view charts on screen as well? (y/n): ").strip().lower() == "y"

            build_category_chart(df)
            save_chart("category_totals.png")
            maybe_show(view_charts)

            build_running_balance_chart(df)
            save_chart("running_balance.png")
            maybe_show(view_charts)

            build_income_vs_expense_chart(df)
            save_chart("income_vs_expense.png")
            maybe_show(view_charts)

if __name__ == "__main__":
    main()