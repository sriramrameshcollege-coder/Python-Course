def main() -> None:
    print("=== Expense Tracker ===")

    transactions = []  # container: list of dicts

    while True:
        raw_amount = input("Enter amount (or 'q' to quit): ")

        if raw_amount.lower() == "q":
            break

        try:
            amount = float(raw_amount)
        except ValueError:
            print("That's not a valid number, try again.")
            continue

        category = input("Enter category (e.g. food, rent, fun): ")

        transaction = {"amount": amount, "category": category}
        transactions.append(transaction)

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

    total = sum(t["amount"] for t in transactions)
    print(f"Total transactions: {len(transactions)}")
    print(f"Net balance: {total}")

    categories = {}  # dict: category -> running total
    for t in transactions:
        categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]

    print("By category:")
    for category, amount in categories.items():
        print(f"  {category}: {amount}")


if __name__ == "__main__":
    main()