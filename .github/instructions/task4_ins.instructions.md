

You are designing a Python class that represents a  **basic bank account system** . The system must allow:

* Creating accounts with an owner name and an initial balance.
* Depositing money.
* Withdrawing money.
* Transferring funds between accounts.
* Restricting users.

You must ensure that this system is:

* **Correct** : Through use of `assert` to validate assumptions in your logic.
* **Safe** : Through defensive programming techniques that prevent invalid inputs (e.g. wrong types, negative amounts).

# Requirements

#### Functionality for the `BankAccount` class:

* Each account has an `owner` (a string) and a non-negative starting `balance` (float or int) and an `account_number` (a int).
* Users can deposit, withdraw, and transfer funds.
* Account ID is a unique number associated with each account. Each account should have an account number should proceed the previous by 1. Account numbers start from 1045.
* Every user at Goldman Stanley is gifted $49.99 upon opening their account.
  * Morgan Stanley will likely build upon this codebase later on and introduce other subclasses of `BankAccount` for their other financial products that may offer different opening bonuses.

To facilitate this you will need minimally the below listed methods and a class itself called `BankAccount` as well as it's constructor.

`set_next_account_number(cls, next_account_number: int) -> None`

In testing your code you will need to create many instance of bank accounts, quite often in your testing it will be useful to reset / update what the next account number is. You can assume this method will be called before each unit test. e.g `BankAccount.set_next_account_number(1045)`

1. Set's the account number for the next account that will be created.
2. Method is a class method.

You can assume if this method is called then you can ignore previous instances.

`ban_account(self, reason:str) -> None`

* This method is used to flag an account as banned (e.g., due to suspicious activity or internal audit findings).
* Once banned, the user  **cannot deposit, withdraw, or transfer funds** .
* All affected methods should check whether the account is banned and raise an error if any operation is attempted.
* All banned users have their account number stored within `BankAccount.banned_accounts` .
* A reason is always provided however maybe an empty string.
  * This method is demonstrated in the string example below.

**Update** 20/05/2025:

As this behaviour was not initially defined in the spec we will accept a reasonable interpretation as to not invalidate past attempts see following:

Calling the `ban_account` method on an already banned account you have the choice of:

* Not raising an error, but updating the reason to be the new reason.
* Raising a relevant error.

`unban_all(cls) -> None`

* After this method is called all accounts are no longer banned. Similar to `set_next_account_number` you can assume this method will be called before each test and is also a class method.

`deposit(self, amount: float | int) -> None`

* Adds a specified non-negative amount to the account balance.

`withdraw(self, amount: float | int) -> None`

* Deducts a specified non-negative amount from the account balance if sufficient funds are available.

#### `transfer_to(self, target_account: "BankAccount", amount: float | int) -> None`

* Transfers a non-negative amount to another valid `BankAccount` instance, provided enough funds exist.

`set_transaction_limit(self, limit: float | int | None) -> None`

* Allows the account to specify a maximum transaction amount for withdrawals or transfers.
* Withdrawals or transfers that exceed this limit, even if funds are available, should not proceed.
* By default an account's limit is `None`.
  * If `None` is being passed in as the limit this is essentially removing a previous limit.
    * If the limit was already `None` do not raise any errors.

`is_banned(self) -> bool`

1. Returns `True` if the account is banned and `False` if the account is not banned.

`__str__(self) -> str:`

Please follow the code snippet below for the correct formatting for the `BankAccount`'s string method:

```python
account1 = BankAccount("RE", 1000)
account2 = BankAccount("CC", 10**7)
account3 = BankAccount("Gary", 70.33)

account2.set_transaction_limit(10)
account3.ban_account("Suspicious activity")

print(account1)
print(account2)
print(account3)
```

Outputs:

```plaintext
RE's account (1045): Balance=$1,049.99 | Limit=$N/A | Banned=No
CC's account (1046): Balance=$10,000,049.99 | Limit=$10.00 | Banned=No
Gary's account (1047): Balance=$120.32 | Limit=$N/A | Banned=Yes | Ban Reason: Suspicious activity
```

All numbers in the `__str__` method should be displayed as a float with two decimal places.


## Defensive Programming:

* `CustomTypeError`:
  * A value is the wrong type (e.g. a string instead of a float or int).
* `CustomValueError`:
  * A value is of the correct type but invalid (e.g. negative balance or amount).
* `CustomOperationError` :
  * A transaction has been requested with at least one flagged user.
* `CustomLimitError`:
  * Exceeding the transaction limit should raise a `CustomLimitError`.
* `CustomKeyError`:
  * Occurs when you try to access a key in the dictionary that doesn't exist.

#### Assertions:

* Use `assert` to verify internal state:
  * Within each method you should check appropriate variables are within a valid range after performing operations. E.g. check the balance has decreased after a withdrawal.


# Examples

## Example 1 (Valid usage)

```python
alice = BankAccount("Alice", 100)
bob = BankAccount("Bob", 50)

alice.deposit(50)      
# Alice now has 199.99 (100 + 50 + 49.99)
alice.withdraw(20)     
# Alice now has 179.99
alice.transfer_to(bob, 30)  
# Alice has 149.99, Bob has 129.99
```



## Example 2 (invalid usage)

```python
acc = BankAccount("Charlie", 100)

acc.deposit("fifty") # CustomTypeError: Deposit amount must be a number
acc.deposit(-10) # CustomValueError: Deposit amount must be non-negative

```


## Example 3 (more invalid usage)

```python
acc1 = BankAccount("Dana", 40)
acc2 = BankAccount("Eli", 40)
# AssertionError: Cannot transfer more than available balance
acc1.transfer_to(acc2, 100) 
# CustomTypeError: Target must be a BankAccount instance
acc1.transfer_to("not-an-account", 10)

```
