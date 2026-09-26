# Expense Tracker

A simple command-line tool to track income and expenses, see summaries, and visualize spending. Built as a final project for the Intro to Python course.

## What it does

You can log transactions as income, expenses, or recurring transactions (like a monthly salary or rent), and the tool keeps track of everything in a CSV file so your data persists between runs. Once you've logged some transactions, it gives you a full breakdown: totals by category, running balance over time, and some quick statistics like your average income vs. average expense.

## How it's built

Tracking money in and money out naturally called for two related but distinct kinds of transactions, so `Income` and `Expense` are built as separate classes that share a common `Transaction` base, this made it easy to fix an early bug where the sign of a transaction (positive or negative) was tied to how the user typed the number, instead of what kind of transaction it actually was. Recurring transactions (like rent or salary) needed the same income/expense split *plus* a frequency label, so that's handled with a small mixin class combined via multiple inheritance, rather than duplicating logic across four separate classes.

For the numbers, `numpy` handles statistics like average and biggest transaction, separately for income and expenses, since mixing the two together produced numbers that didn't mean anything on their own. Transaction data is saved and reloaded from a CSV file, and `pandas` is used to group and summarize that data by category and type once it's loaded back in.

To actually see spending patterns, the tool uses `matplotlib` to generate a few charts: a bar chart of totals by category, a line chart showing how the balance changed over time, and a pie chart comparing total income to total expenses. Charts are automatically saved as `.png` files in the `output/` folder every time the program runs, and are committed to this repository so they're viewable without needing to run anything:

- [`output/category_totals.png`](output/category_totals.png) — total spending/income by category
- [`output/running_balance.png`](output/running_balance.png) — balance over time
- [`output/income_vs_expense.png`](output/income_vs_expense.png) — income vs. expense split

You can also optionally view them interactively in a pop-up window while the program runs.

## Getting started

This project uses [uv](https://docs.astral.sh/uv/) for dependency management, and is installable via `pyproject.toml`.

```bash
# Clone the repo
git clone https://github.com/sriramrameshcollege-coder/Python-Course.git
cd Python-Course

# Install the package
uv pip install -e .

# Run it (as a module)
uv run -m expense_tracker

# Or, via the installed CLI command
uv run expense-tracker
```

## Project structure

```
src/expense_tracker/
├── __init__.py   # exposes key classes/functions for direct import
├── __main__.py   # entry point for `uv run -m expense_tracker`
├── main.py       # CLI loop and program logic
├── models.py     # Transaction, Income, Expense, Recurring classes
├── storage.py    # save/load transactions, category filtering
├── analysis.py   # numpy statistics, pandas summaries
└── viz.py        # matplotlib charts (auto-saved to output/)
```

## Code quality

This project uses [ruff](https://astral.sh/ruff) for linting and formatting to follow PEP-8 style guidelines:

```bash
uv run ruff check src/
uv run ruff format src/
```