# Task 9: Banking System - OOP Foundations
# Approach: BankAccount class with private balance, property/setter for controlled
# access, validated deposit/withdraw, classmethod for interest, staticmethod for
# validation helper, __str__ and __repr__ for readable output.

class BankAccount:
    # class attribute - shared across all accounts
    bank_name = "National Bank of Pakistan"
    total_accounts = 0

    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.__balance = 0   # private - can't access directly from outside
        self.__transactions = []

        # use deposit method to validate initial balance
        if initial_balance > 0:
            self.deposit(initial_balance)

        BankAccount.total_accounts += 1
        self.__account_number = f"NBP-{1000 + BankAccount.total_accounts}"
        self.__transactions = []

    # property to allow reading balance but not setting it directly
    @property
    def balance(self):
        return self.__balance

    @property
    def account_number(self):
        return self.__account_number

    # validated deposit
    def deposit(self, amount):
        if not BankAccount.is_valid_amount(amount):
            raise ValueError(f"Invalid deposit amount: {amount}")
        self.__balance += amount
        self.__transactions.append(("DEPOSIT", amount, self.__balance))
        print(f"  [+] Deposited Rs. {amount:,.0f} | New Balance: Rs. {self.__balance:,.0f}")

    # validated withdrawal
    def withdraw(self, amount):
        if not BankAccount.is_valid_amount(amount):
            raise ValueError(f"Invalid withdrawal amount: {amount}")
        if amount > self.__balance:
            raise ValueError(f"Insufficient funds. Balance: Rs. {self.__balance:,.0f}")
        self.__balance -= amount
        self.__transactions.append(("WITHDRAW", amount, self.__balance))
        print(f"  [-] Withdrew Rs. {amount:,.0f} | New Balance: Rs. {self.__balance:,.0f}")

    def get_statement(self):
        print(f"\n  --- Statement for {self.owner} ({self.__account_number}) ---")
        if not self.__transactions:
            print("  No transactions yet.")
        for t_type, amount, bal_after in self.__transactions:
            sign = "+" if t_type == "DEPOSIT" else "-"
            print(f"  {t_type:<10} {sign}Rs. {amount:>10,.0f}   Balance: Rs. {bal_after:>10,.0f}")
        print(f"  Current Balance: Rs. {self.__balance:,.0f}")

    # classmethod - knows about the class, not just the instance
    @classmethod
    def apply_annual_interest(cls, account, rate=0.05):
        interest = round(account.balance * rate, 2)
        account.deposit(interest)
        print(f"  [Interest] {rate*100}% applied to {account.owner}'s account")

    # staticmethod - utility, doesn't need self or cls
    @staticmethod
    def is_valid_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    def __str__(self):
        return f"Account[{self.__account_number}] | Owner: {self.owner} | Balance: Rs. {self.__balance:,.0f}"

    def __repr__(self):
        return f"BankAccount(owner='{self.owner}', account='{self.__account_number}', balance={self.__balance})"


# ---- Demo ----
print("=" * 55)
print("         BANKING SYSTEM - OOP Demo")
print("=" * 55)

print(f"\nBank: {BankAccount.bank_name}\n")

# create accounts
acc1 = BankAccount("Ali Hassan", 50000)
acc2 = BankAccount("Sara Khan", 20000)

print()

# transactions on acc1
print(f"--- Operations on {acc1.owner}'s account ---")
acc1.deposit(15000)
acc1.withdraw(8000)
acc1.withdraw(5000)

print()

# transactions on acc2
print(f"--- Operations on {acc2.owner}'s account ---")
acc2.deposit(30000)

try:
    acc2.withdraw(999999)   # should fail
except ValueError as e:
    print(f"  [ERROR] {e}")

print()

# apply interest
print("--- Applying Annual Interest (5%) ---")
BankAccount.apply_annual_interest(acc1)
BankAccount.apply_annual_interest(acc2, rate=0.07)

print()

# statements
acc1.get_statement()
acc2.get_statement()

print()

# __str__ and __repr__
print("--- Print accounts ---")
print(acc1)
print(acc2)
print()
print("repr output:")
print(repr(acc1))

# can't access private balance directly
print(f"\nTotal accounts opened: {BankAccount.total_accounts}")

# this would raise an AttributeError:
try:
    print(acc1.__balance)
except AttributeError as e:
    print(f"\nDirect access to __balance: BLOCKED -> {e}")
