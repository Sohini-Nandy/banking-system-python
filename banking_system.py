import json
import random
import hashlib
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("accounts.json")


def load_accounts():
    """Load saved accounts from accounts.json."""
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read account data. Starting with empty data.")
        return {}


def save_accounts(accounts):
    """Save all accounts to accounts.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def hash_pin(pin):
    """Convert a PIN into a hash before storing it."""
    return hashlib.sha256(pin.encode()).hexdigest()


def valid_pin(pin):
    return pin.isdigit() and len(pin) == 4


def generate_account_number(accounts):
    """Generate a unique 10-digit account number."""
    while True:
        account_number = str(random.randint(1000000000, 9999999999))
        if account_number not in accounts:
            return account_number


def add_transaction(account, transaction_type, amount, details=""):
    transaction = {
        "type": transaction_type,
        "amount": round(amount, 2),
        "details": details,
        "date_time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    }
    account["transactions"].append(transaction)


def create_account(accounts):
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter your name: ").strip()

    phone = input("Enter phone number: ").strip()
    while not (phone.isdigit() and len(phone) == 10):
        print("Please enter a valid 10-digit phone number.")
        phone = input("Enter phone number: ").strip()

    pin = input("Create a 4-digit PIN: ").strip()
    while not valid_pin(pin):
        print("PIN must contain exactly 4 digits.")
        pin = input("Create a 4-digit PIN: ").strip()

    confirm_pin = input("Confirm your PIN: ").strip()
    while confirm_pin != pin:
        print("PINs do not match.")
        confirm_pin = input("Confirm your PIN: ").strip()

    account_number = generate_account_number(accounts)

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": hash_pin(pin),
        "balance": 0.0,
        "transactions": []
    }

    save_accounts(accounts)

    print("\nAccount created successfully!")
    print(f"Your Account Number is: {account_number}")
    print("Please keep your account number and PIN safe.")


def login(accounts):
    print("\n========== LOGIN ==========")
    account_number = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    account = accounts.get(account_number)

    if account and account["pin"] == hash_pin(pin):
        print(f"\nLogin successful. Welcome, {account['name']}!")
        return account_number

    print("Invalid Account Number or PIN.")
    return None


def check_balance(account):
    print("\n========== BALANCE ==========")
    print(f"Current Balance: ₹{account['balance']:.2f}")


def deposit(account):
    print("\n========== DEPOSIT ==========")

    try:
        amount = float(input("Enter amount to deposit: ₹"))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        account["balance"] += amount
        add_transaction(account, "Deposit", amount, "Money deposited")
        print(f"₹{amount:.2f} deposited successfully.")
        print(f"New Balance: ₹{account['balance']:.2f}")
    except ValueError:
        print("Please enter a valid amount.")


def withdraw(account):
    print("\n========== WITHDRAW ==========")

    try:
        amount = float(input("Enter amount to withdraw: ₹"))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        if amount > account["balance"]:
            print("Insufficient balance.")
            return

        account["balance"] -= amount
        add_transaction(account, "Withdrawal", amount, "Money withdrawn")
        print(f"₹{amount:.2f} withdrawn successfully.")
        print(f"Remaining Balance: ₹{account['balance']:.2f}")
    except ValueError:
        print("Please enter a valid amount.")


def transfer(accounts, sender_number):
    print("\n========== TRANSFER MONEY ==========")

    receiver_number = input("Enter receiver Account Number: ").strip()

    if receiver_number == sender_number:
        print("You cannot transfer money to your own account.")
        return

    if receiver_number not in accounts:
        print("Receiver account not found.")
        return

    try:
        amount = float(input("Enter amount to transfer: ₹"))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        sender = accounts[sender_number]
        receiver = accounts[receiver_number]

        if amount > sender["balance"]:
            print("Insufficient balance.")
            return

        sender["balance"] -= amount
        receiver["balance"] += amount

        add_transaction(
            sender,
            "Transfer Sent",
            amount,
            f"Transferred to Account {receiver_number}"
        )
        add_transaction(
            receiver,
            "Transfer Received",
            amount,
            f"Received from Account {sender_number}"
        )

        save_accounts(accounts)

        print(f"₹{amount:.2f} transferred successfully.")
        print(f"Your New Balance: ₹{sender['balance']:.2f}")

    except ValueError:
        print("Please enter a valid amount.")


def transaction_history(account):
    print("\n========== TRANSACTION HISTORY ==========")

    transactions = account["transactions"]

    if not transactions:
        print("No transactions found.")
        return

    for number, transaction in enumerate(transactions, start=1):
        print(
            f"{number}. {transaction['date_time']} | "
            f"{transaction['type']} | "
            f"₹{transaction['amount']:.2f} | "
            f"{transaction['details']}"
        )


def change_pin(account):
    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter old PIN: ").strip()

    if account["pin"] != hash_pin(old_pin):
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    while not valid_pin(new_pin):
        print("New PIN must contain exactly 4 digits.")
        new_pin = input("Enter new 4-digit PIN: ").strip()

    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("PINs do not match. PIN was not changed.")
        return

    if new_pin == old_pin:
        print("New PIN must be different from the old PIN.")
        return

    account["pin"] = hash_pin(new_pin)
    save_accounts(accounts_global)

    print("PIN changed successfully.")


def account_menu(accounts, account_number):
    account = accounts[account_number]

    while True:
        print("\n======================================")
        print("             ACCOUNT MENU")
        print("======================================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(account)
        elif choice == "2":
            deposit(account)
            save_accounts(accounts)
        elif choice == "3":
            withdraw(account)
            save_accounts(accounts)
        elif choice == "4":
            transfer(accounts, account_number)
        elif choice == "5":
            transaction_history(account)
        elif choice == "6":
            change_pin(account)
        elif choice == "7":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please select 1-7.")


def main():
    global accounts_global
    accounts_global = load_accounts()

    while True:
        print("\n======================================")
        print("          PYTHON BANKING SYSTEM")
        print("======================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account(accounts_global)
        elif choice == "2":
            account_number = login(accounts_global)
            if account_number:
                account_menu(accounts_global, account_number)
        elif choice == "3":
            print("Thank you for using the Banking System.")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
