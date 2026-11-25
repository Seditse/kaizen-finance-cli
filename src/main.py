
# KAIZEN FINANCE CLI
# Project 01 - Project Kaizen

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "transactions.json"

transactions = []


def load_transactions():
    """Load existing transactions from the JSON file."""
    global transactions

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            transactions = json.load(file)

    except FileNotFoundError:
        transactions = []

    except json.JSONDecodeError:
        print("Warning: Transaction file is invalid. Starting with empty records.")
        transactions = []


def save_transactions():
    """Save transactions to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)


def display_welcome():
    print("=" * 40)
    print("       K A I Z E N   F I N A N C E")
    print("=" * 40)
    print("Welcome to your personal finance manager!")
    print()


def display_menu():
    print("\nMAIN MENU")
    print("1. Add income")
    print("2. Add expense")
    print("3. View transactions")
    print("4. View balance")
    print("5. Exit")


def add_transaction(transaction_type):
    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount (P): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    transaction = {
        "type": transaction_type,
        "description": description,
        "amount": amount
    }

    transactions.append(transaction)
    save_transactions()

    print(f"{transaction_type.capitalize()} recorded successfully!")


def view_transactions():
    if not transactions:
        print("No transactions recorded yet.")
        return

    print("\nTRANSACTION HISTORY")
    print("-" * 55)

    for transaction in transactions:
        print(
            f"{transaction['type'].capitalize():10} | "
            f"{transaction['description']:20} | "
            f"P{transaction['amount']:.2f}"
        )


def view_balance():
    income = 0
    expenses = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            income += transaction["amount"]
        else:
            expenses += transaction["amount"]

    balance = income - expenses

    print("\nFINANCIAL SUMMARY")
    print("-" * 30)
    print(f"Total income:    P{income:.2f}")
    print(f"Total expenses:  P{expenses:.2f}")
    print(f"Current balance: P{balance:.2f}")


def main():
    load_transactions()
    display_welcome()

    while True:
        display_menu()

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            add_transaction("income")

        elif choice == "2":
            add_transaction("expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            print("Thank you for using Kaizen Finance!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
