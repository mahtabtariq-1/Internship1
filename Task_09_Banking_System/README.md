# Task 09 — Banking System

## Topic
OOP: Foundations

## What This Task Does
A `BankAccount` class that stores an owner name and balance securely.
The balance is inaccessible from outside the class. Deposits and withdrawals
go through validated methods only. Printing any account gives a clean, readable summary.

## Concepts Used
- Defining classes, `__init__()`, `self`
- Instance attributes vs class attributes (`bank_name`, `total_accounts`)
- Instance methods (`deposit`, `withdraw`, `get_statement`)
- `@classmethod` — `apply_annual_interest`
- `@staticmethod` — `is_valid_amount`
- `__private` naming convention (`__balance`, `__transactions`)
- `@property` for controlled read access to balance
- `__str__()` and `__repr__()` for readable output

## How to Run
```bash
python banking_system.py
```

## Sample Output
```
[+] Deposited Rs. 50,000 | New Balance: Rs. 50,000
[-] Withdrew Rs. 8,000 | New Balance: Rs. 57,000
[ERROR] Insufficient funds. Balance: Rs. 50,000

Account[NBP-1001] | Owner: Ali Hassan | Balance: Rs. 54,600

Direct access to __balance: BLOCKED
```
