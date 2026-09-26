from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = Path("output")


def build_category_chart(df: pd.DataFrame) -> None:
    """Build (but don't show/save) a bar chart of total signed amount per category."""
    totals = df.groupby("category")["signed_amount"].sum().sort_values()
    colors = ["tab:red" if v < 0 else "tab:green" for v in totals.values]

    plt.figure(figsize=(8, 5))
    plt.barh(totals.index, totals.values, color=colors)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlabel("Amount")
    plt.title("Total by Category")
    plt.tight_layout()


def build_running_balance_chart(df: pd.DataFrame) -> None:
    """Build (but don't show/save) a line chart of cumulative balance."""
    running = df["signed_amount"].cumsum()

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(running) + 1), running.values, marker="o")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Transaction number")
    plt.ylabel("Balance")
    plt.title("Running Balance Over Time")
    plt.tight_layout()


def save_chart(filename: str) -> None:
    """Save the current figure to output/<filename>."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / filename)
    print(f"Saved to output/{filename}")


def maybe_show(view_interactively: bool) -> None:
    """Optionally display the current figure interactively."""
    if view_interactively:
        plt.show()
    plt.close()

def build_income_vs_expense_chart(df: pd.DataFrame) -> None:
    """Build (but don't show/save) a pie chart comparing total income vs total expense."""
    total_income = df.loc[df["signed_amount"] > 0, "signed_amount"].sum()
    total_expense = -df.loc[df["signed_amount"] < 0, "signed_amount"].sum()

    plt.figure(figsize=(6, 6))
    plt.pie(
        [total_income, total_expense],
        labels=["Income", "Expense"],
        colors=["tab:green", "tab:red"],
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Income vs Expense")
    plt.tight_layout()