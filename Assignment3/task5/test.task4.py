"""
Although this file is named test_task4.py it is where you will work
for task 5.
The provided testcase is quite verbose and not all tests should be as
detailed in their documentation.

Please also note that the provided example only provides one "test"
this would be marked as unsatisfactory. Please include multiple different cases for each test.
"""

import unittest
from task4 import BankAccount  # assume this is the provided class
from custom_errors import *


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Reset banned accounts and account number before each test
        BankAccount.banned_accounts.clear()
        BankAccount.set_next_account_number(1045)

        # Create test accounts that will be used across multiple tests
        self.account1 = BankAccount("Alice Smith", 1000)
        self.account2 = BankAccount("Bob Johnson", 500)

    def tearDown(self):
        """Clean up after each test method."""  # Clear banned accounts to ensure test isolation
        BankAccount.banned_accounts.clear()

    # INITIALIZATION TESTS

    def test_valid_account_creation(self):
        """Test creating accounts with valid parameters"""
        # Test with integer balance
        account1 = BankAccount("John Doe", 1000)
        self.assertEqual(account1.owner, "John Doe")
        self.assertEqual(account1.balance, 1049.99)  # 1000 + 49.99 bonus
        self.assertIsInstance(account1.account_number, int)
        self.assertGreaterEqual(account1.account_number, 1045)

        # Test with float balance
        account2 = BankAccount("Jane Smith", 500.50)
        self.assertEqual(
            account2.balance, 550.49
        )  # 500.50 + 49.99 bonus        # Test with zero balance
        account3 = BankAccount("Zero Balance", 0)
        self.assertEqual(account3.balance, 49.99)  # 0 + 49.99 bonus

    def test_invalid_owner_type(self):
        """Test creating account with invalid owner type"""
        with self.assertRaises(CustomTypeError):
            BankAccount(123, 1000)
        with self.assertRaises(CustomTypeError):
            BankAccount(None, 1000)

    def test_negative_initial_balance(self):
        """Test creating account with negative balance"""
        with self.assertRaises(CustomValueError):
            BankAccount("John Doe", -100)

    # DEPOSIT TESTS

    def test_valid_deposit(self):
        """
        1.1 Valid deposit.
        Test the deposit method of the BankAccount class to ensure it correctly adds
        the deposited amount to the account balance.

        Steps:
        1. Create a BankAccount instance with an initial balance of 1000 (+ 49.99 the bonus amount).
        2. Deposit 500 into the account.
        3. Assert that the account balance is updated to 1549.99 (Inital 1000 + 49.99 (from the bonus) + 500 (from the deposit)).

        Assertion:
        - Verify that the account balance after the deposit is 1549.99, indicating
          that the deposit method works as expected.
        """
        account = BankAccount("John Doe", 1000)
        account.deposit(500)
        self.assertEqual(
            account.balance,
            1549.99,
            f"Deposit method failed to update balance correctly. Expected 1549.99, got {account.balance}",
        )

    def test_deposit_multiple_amounts(self):
        """Test depositing different types of amounts"""
        self.account1.deposit(100)
        self.assertEqual(self.account1.balance, 1149.99)

        self.account1.deposit(25.50)
        self.assertEqual(self.account1.balance, 1175.49)

        self.account1.deposit(0)  # Zero deposit should be allowed
        self.assertEqual(self.account1.balance, 1175.49)

    def test_invalid_balance_type(self):
        """1.2 Check bank init balance type assertion"""
        # Example of how to check if an error is being raised
        with self.assertRaises(
            CustomTypeError,
            msg="Expected a type error to be raised when making a bank account with the balance 'fifty'. Either no error or the incorrect error was raised.",
        ):
            BankAccount("Rupert", "fifty")

    def test_negative_deposit(self):
        """Test depositing negative amounts"""
        with self.assertRaises(CustomValueError):
            self.account1.deposit(-50)

    def test_deposit_to_banned_account(self):
        """Test depositing to a banned account"""
        self.account1.ban_account("Fraudulent activity")
        with self.assertRaises(CustomOperationError):
            self.account1.deposit(100)

    # WITHDRAWAL TESTS

    def test_valid_withdrawal(self):
        """Test valid withdrawals"""
        original_balance = self.account1.balance
        self.account1.withdraw(200)
        self.assertEqual(self.account1.balance, original_balance - 200)

        # Test withdrawal of exact balance
        self.account2.withdraw(self.account2.balance)
        self.assertEqual(self.account2.balance, 0)

    def test_withdrawal_insufficient_funds(self):
        """Test withdrawal exceeding balance"""
        with self.assertRaises(CustomValueError):
            self.account2.withdraw(600)  # account2 has 549.99 balance

    def test_invalid_withdrawal_type(self):
        """Test withdrawal with invalid types"""
        with self.assertRaises(CustomTypeError):
            self.account1.withdraw("100")
        with self.assertRaises(CustomTypeError):
            self.account1.withdraw([100])

    def test_negative_withdrawal(self):
        """Test negative withdrawal amounts"""
        with self.assertRaises(CustomValueError):
            self.account1.withdraw(-50)

    def test_withdrawal_from_banned_account(self):
        """Test withdrawal from banned account"""
        self.account1.ban_account("Suspicious activity")
        with self.assertRaises(CustomOperationError):
            self.account1.withdraw(100)

    def test_withdrawal_exceeds_limit(self):
        """Test withdrawal exceeding transaction limit"""
        self.account1.set_transaction_limit(300)
        with self.assertRaises(CustomLimitError):
            self.account1.withdraw(400)

    #  TRANSFER TESTS

    def test_valid_transfer(self):
        """Test valid transfers between accounts"""
        sender_balance = self.account1.balance
        target_balance = self.account2.balance
        transfer_amount = 200

        self.account1.transfer_to(self.account2, transfer_amount)

        self.assertEqual(self.account1.balance, sender_balance - transfer_amount)
        self.assertEqual(self.account2.balance, target_balance + transfer_amount)

    def test_transfer_insufficient_funds(self):
        """Test transfer exceeding sender balance"""
        with self.assertRaises(CustomValueError):
            self.account2.transfer_to(self.account1, 600)

    def test_transfer_invalid_target_type(self):
        """Test transfer with invalid target account type"""
        with self.assertRaises(CustomTypeError):
            self.account1.transfer_to("not_an_account", 100)
        with self.assertRaises(CustomTypeError):
            self.account1.transfer_to(None, 100)

    def test_transfer_invalid_amount_type(self):
        """Test transfer with invalid amount type"""
        with self.assertRaises(CustomTypeError):
            self.account1.transfer_to(self.account2, "100")

    def test_transfer_negative_amount(self):
        """Test transfer with negative amount"""
        with self.assertRaises(CustomValueError):
            self.account1.transfer_to(self.account2, -50)

    def test_transfer_from_banned_account(self):
        """Test transfer from banned account"""
        self.account1.ban_account("Fraud detected")
        with self.assertRaises(CustomOperationError):
            self.account1.transfer_to(self.account2, 100)

    def test_transfer_to_banned_account(self):
        """Test transfer to banned account"""
        self.account2.ban_account("Account frozen")
        with self.assertRaises(CustomOperationError):
            self.account1.transfer_to(self.account2, 100)

    def test_transfer_exceeds_limit(self):
        """Test transfer exceeding transaction limit"""
        self.account1.set_transaction_limit(150)
        with self.assertRaises(CustomLimitError):
            self.account1.transfer_to(self.account2, 200)

    #  TRANSACTION LIMIT TESTS

    def test_set_valid_transaction_limit(self):
        """Test setting valid transaction limits"""
        self.account1.set_transaction_limit(500)
        self.assertEqual(self.account1.transaction_limit, 500)

        self.account1.set_transaction_limit(100.50)
        self.assertEqual(self.account1.transaction_limit, 100.50)

        self.account1.set_transaction_limit(None)
        self.assertIsNone(self.account1.transaction_limit)

    def test_set_invalid_transaction_limit_type(self):
        """Test setting invalid transaction limit types"""
        with self.assertRaises(CustomTypeError):
            self.account1.set_transaction_limit("500")
        with self.assertRaises(CustomTypeError):
            self.account1.set_transaction_limit([500])

    def test_set_negative_transaction_limit(self):
        """Test setting negative transaction limit"""
        with self.assertRaises(CustomValueError):
            self.account1.set_transaction_limit(-100)

    #  BANNING TESTS

    def test_ban_account(self):
        """Test banning accounts"""
        self.assertFalse(self.account1.is_banned())
        self.account1.ban_account("Fraudulent activity")
        self.assertTrue(self.account1.is_banned())
        self.assertEqual(self.account1.ban_reason, "Fraudulent activity")
        self.assertIn(self.account1.account_number, BankAccount.banned_accounts)

    def test_ban_account_invalid_reason_type(self):
        """Test banning account with invalid reason type"""
        with self.assertRaises(CustomTypeError):
            self.account1.ban_account(123)
        with self.assertRaises(CustomTypeError):
            self.account1.ban_account(None)

    def test_is_banned_false_for_new_account(self):
        """Test that new accounts are not banned"""
        new_account = BankAccount("New User", 100)
        self.assertFalse(new_account.is_banned())

    #  CLASS METHOD TESTS

    def test_set_next_account_number(self):
        """Test setting next account number"""
        BankAccount.set_next_account_number(2000)
        new_account = BankAccount("Test User", 100)
        self.assertEqual(new_account.account_number, 2000)

        # Test invalid type
        with self.assertRaises(CustomTypeError):
            BankAccount.set_next_account_number("2000")

    def test_unban_all(self):
        """Test unbanning all accounts"""
        self.account1.ban_account("Test reason 1")
        self.account2.ban_account("Test reason 2")
        self.assertTrue(self.account1.is_banned())
        self.assertTrue(self.account2.is_banned())

        BankAccount.unban_all()
        self.assertFalse(self.account1.is_banned())
        self.assertFalse(self.account2.is_banned())
        self.assertEqual(len(BankAccount.banned_accounts), 0)

    #  STRING REPRESENTATION TESTS

    def test_str_representation(self):
        """Test string representation of accounts"""
        account_str = str(self.account1)
        self.assertIn("Alice Smith", account_str)
        self.assertIn("$1,049.99", account_str)
        self.assertIn("Banned=No", account_str)
        # Test banned account string representation
        self.account1.ban_account("Test ban")
        account_str = str(self.account1)
        self.assertIn("Banned=Yes", account_str)
        self.assertIn("Ban Reason: Test ban", account_str)


if __name__ == "__main__":
    unittest.main()
