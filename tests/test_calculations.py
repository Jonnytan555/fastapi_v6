# import pytest
# from app.calculations import InsufficientFundsError, add, divide, multiply
# from app.calculations import subtract
# from app.calculations import BankAccount
#
# @ pytest.fixture
# def zero_bank_account() -> BankAccount:
#     return BankAccount(0)
#
# @ pytest.fixture
# def bank_account() -> BankAccount:
#     return BankAccount(100)
#
# @pytest.mark.parametrize("num1, num2, expected", [
#     (2, 2, 4),
#     (-1, 2, 1),
#     (-1, -6, -7),
#     (1000000, 2000000, 3000000),
# ])
# def test_addition(num1, num2, expected):
#     assert add(num1, num2) == expected
#
# # def test_addition_negative():
# #     print('testing add function with negative numbers')
# #     assert add(-2, -3) == -5
#
# # def test_addition_zero():
# #     print('testing add function with zero')
# #     assert add(0, 5) == 5
#
# # def test_addition_large_numbers():
# #     print('testing add function with large numbers')
# #     assert add(1000000, 2000000) == 3000000
#
# def test_subtraction():
#     print('testing subtract function')
#     assert subtract(5, 3) == 2
#
# def test_division():
#     print('testing subtract function')
#     assert divide(10, 2) == 5
#
# def test_multiply():
#     print('testing multiply function')
#     assert multiply(10, 2) == 20
#
# def test_bank_set_initial_amount():
#     account = BankAccount(100) # type: ignore
#     assert account.balance == 100
#
# # def test_bank_default_initial_amount():
# #     account = BankAccount() # type: ignore
# #     assert account.balance == 0
#
# def test_bank_default_initial_amount(zero_bank_account: BankAccount):
#     assert zero_bank_account.balance == 0
#
# def test_withdrawl(bank_account):
#
#     bank_account.withdraw(50)
#     assert bank_account.balance == 50
#
# def test_deposit(bank_account):
#     bank_account.deposit(50)
#     assert bank_account.balance == 150
#
# def test_collect_interest(bank_account):
#     bank_account.collect_interest()
#     assert round(bank_account.balance, 6) == 110.0
#
# def test_insufficient_funds(bank_account):
#     with pytest.raises(InsufficientFundsError):
#         bank_account.withdraw(200)
#
#
#
#
