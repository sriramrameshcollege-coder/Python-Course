def main() -> None:
    print("=== Expense Tracker ===")

    while True:
        raw_amount = input("Enter amount (or 'q' to quit): ")

        if raw_amount.lower() == "q":
            print("Goodbye!")
            break

        try:
            amount = float(raw_amount)
        except ValueError:
            print("That's not a valid number, try again.")
            continue

        category = input("Enter category (e.g. food, rent, fun): ")

        if amount < 0:
            print(f"Recorded expense: {amount} in {category}")
        else:
            print(f"Recorded income: {amount} in {category}")


if __name__ == "__main__":
    main()