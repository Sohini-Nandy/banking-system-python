# Banking System – Python Mini Project

A beginner-friendly command-line Banking System built in Python for an internship mini project.

## Features
- Create a bank account
- Generate a unique account number
- Login using Account Number and 4-digit PIN
- Check account balance
- Deposit money
- Withdraw money with balance checking
- Transfer money between accounts
- View transaction history with date and time
- Change PIN
- Logout
- Save account data locally in `accounts.json`

## Python Concepts Used
- Variables and data types
- Conditional statements
- Loops
- Functions
- Lists and dictionaries
- String operations
- Modules
- `random`
- `datetime`
- JSON file handling
- Basic PIN hashing with `hashlib`

## Requirements
- Python 3.x
- No external Python packages are required.

## How to Run

Open a terminal in this project folder and run:

```bash
python banking_system.py
```

If your computer uses `python3`, run:

```bash
python3 banking_system.py
```

The program automatically creates `accounts.json` after the first account is created.

## Suggested Testing
1. Create two accounts.
2. Login to the first account.
3. Deposit money.
4. Check balance.
5. Withdraw some money.
6. Transfer money to the second account.
7. Check transaction history.
8. Change the PIN.
9. Logout.
10. Login again using the new PIN.

## Project Structure

```text
Banking_System_Mini_Project/
├── banking_system.py
├── README.md
├── .gitignore
└── accounts.json          # created automatically after running
```

## Internship Submission
Push the project folder to a GitHub repository and submit the repository link through the management Google Form.
