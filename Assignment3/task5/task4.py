from custom_errors import *


class BankAccount:
    """A basic bank account system with defensive programming and security features"""

    _next_account_number = 1045
    banned_accounts = set()

    def __init__(self, owner: str, balance: float | int):
        """Initialize a new bank account with owner name and starting balance"""
        if not isinstance(owner, str):
            raise CustomTypeError("Owner name must be a string")
        if not isinstance(balance, (int, float)):
            raise CustomTypeError("Balance must be a number")

        if balance < 0:
            raise CustomValueError("Initial balance must be non-negative")

        self.owner = owner
        self.balance = float(balance) + 49.99
        self.account_number = BankAccount._next_account_number
        self.transaction_limit = None
        self.ban_reason = None

        BankAccount._next_account_number += 1

        assert self.balance >= 49.99, "Balance should include opening bonus"
        assert self.account_number >= 1045, "Account number should be valid"

    @classmethod
    def set_next_account_number(cls, next_account_number: int) -> None:
        """Set the account number for the next account to be created"""
        if not isinstance(next_account_number, int):
            raise CustomTypeError("Account number must be an integer")
        cls._next_account_number = next_account_number

    @classmethod
    def unban_all(cls) -> None:
        """Remove all accounts from the banned list"""
        cls.banned_accounts.clear()

    def ban_account(self, reason: str) -> None:
        """Ban this account with a given reason"""
        if not isinstance(reason, str):
            raise CustomTypeError("Ban reason must be a string")

        self.ban_reason = reason
        BankAccount.banned_accounts.add(self.account_number)

    def is_banned(self) -> bool:
        """Check if this account is banned"""
        return self.account_number in BankAccount.banned_accounts

    def deposit(self, amount: float | int) -> None:
        """Deposit money into the account"""
        if self.is_banned():
            raise CustomOperationError("Cannot deposit to a banned account")

        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Deposit amount must be a number")

        if amount < 0:
            raise CustomValueError("Deposit amount must be non-negative")

        original_balance = self.balance
        self.balance += amount

        assert (
            self.balance == original_balance + amount
        ), "Balance should increase by deposit amount"

    def withdraw(self, amount: float | int) -> None:
        """Withdraw money from the account"""
        if self.is_banned():
            raise CustomOperationError("Cannot withdraw from a banned account")

        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Withdrawal amount must be a number")

        if amount < 0:
            raise CustomValueError("Withdrawal amount must be non-negative")

        if amount > self.balance:
            raise CustomValueError("Insufficient funds for withdrawal")

        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Withdrawal amount exceeds transaction limit")

        original_balance = self.balance
        self.balance -= amount

        assert (
            self.balance == original_balance - amount
        ), "Balance should decrease by withdrawal amount"
        assert self.balance >= 0, "Balance should not be negative"

    def transfer_to(self, target_account: "BankAccount", amount: float | int) -> None:
        """Transfer money to another bank account"""
        if self.is_banned():
            raise CustomOperationError("Cannot transfer from a banned account")

        if not isinstance(target_account, BankAccount):
            raise CustomTypeError("Target must be a BankAccount instance")

        if target_account.is_banned():
            raise CustomOperationError("Cannot transfer to a banned account")

        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Transfer amount must be a number")

        if amount < 0:
            raise CustomValueError("Transfer amount must be non-negative")

        if amount > self.balance:
            raise CustomValueError("Cannot transfer more than available balance")

        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Transfer amount exceeds transaction limit")

        original_sender_balance = self.balance
        original_target_balance = target_account.balance

        self.balance -= amount
        target_account.balance += amount

        assert (
            self.balance == original_sender_balance - amount
        ), "Sender balance should decrease by transfer amount"
        assert (
            target_account.balance == original_target_balance + amount
        ), "Target balance should increase by transfer amount"
        assert self.balance >= 0, "Sender balance should not be negative"

    def set_transaction_limit(self, limit: float | int | None) -> None:
        """Set a transaction limit for withdrawals and transfers"""
        if limit is not None and not isinstance(limit, (int, float)):
            raise CustomTypeError("Transaction limit must be a number or None")

        if limit is not None and limit < 0:
            raise CustomValueError("Transaction limit must be non-negative")
        self.transaction_limit = limit

    def __str__(self) -> str:
        """Return a string representation of the account"""
        balance_str = f"${self.balance:,.2f}"

        if self.transaction_limit is None:
            limit_str = "$N/A"
        else:
            limit_str = f"${self.transaction_limit:,.2f}"

        if self.is_banned():
            banned_str = "Yes"
            ban_reason_str = f" | Ban Reason: {self.ban_reason}"
        else:
            banned_str = "No"
            ban_reason_str = ""

        return f"{self.owner}'s account ({self.account_number}): Balance={balance_str} | Limit={limit_str} | Banned={banned_str}{ban_reason_str}"
