The test case name is taken from the first line in the docstring. Please note that there are no automated marks associated with this task you are marked on the quality and coverage of your tests.

# Description

You are again working on the `BankAccount` class. Your goal is to write a suite of unit tests that cover a wide range of normal and edge-case behaviours which will check your work from the previous task.

You must:

* Write test cases for each public method outlined in the previous task.
* Test for **both** correct and incorrect inputs.
* Use `assertEqual`, `assertRaises`, and (optionally) other assertions like `assertIsInstance`, `assertGreaterEqual`, etc.
* Organise your tests using a testing framework such as `unittest`.

## Requirements

* **✅Some Examples of Positive Cases:**
  * Check depositing and withdrawing valid amounts updates the balance correctly.
  * Check transferring between two valid accounts works as expected.
  * Check flagging / banning accounts prevents deposit/withdraw/transfer involving these accounts.
* ❌ **Negative Cases:**
  * Check Deposit/withdraw/transfer with invalid types & values.
* 🧪 **Test Structure:**
  * Group related tests into test methods.

Remember, same as last task you should be using the errors from `custom_errors.py`

In order to be eligible to get full marks for this task you must make meaningful usage of the setup and teardown functionality provided in the unit test framework. More details here: [https://docs.python.org/3/library/unittest.html#setupclass-and-teardownclass](https://docs.python.org/3/library/unittest.html#setupclass-and-teardownclass)


## Examples

A sample unit test has been provided within the scaffold.
