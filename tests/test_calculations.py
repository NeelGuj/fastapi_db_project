from app.calculations import add, BankAccount
import pytest

'''
The bank_account fixture creates and returns an instance of the BankAccount class with an initial balance of 50. 
This fixture can be used in multiple test functions to avoid duplicating the setup code for creating a BankAccount instance.

How It Works
Decorator: The @pytest.fixture decorator tells pytest that the bank_account function is a fixture.
Reusable Setup: When a test function includes bank_account as an argument, pytest automatically calls this fixture function and provides the returned value (a BankAccount instance) to the test.
                Thus fixture function runs first and returns the value to the test function which is an instance of BankAccount(50).
'''
@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.fixture
def zero_bank_account():
    return BankAccount()




# def test_add():
#     assert add(1, 2) == 3

# If we want to test multiple cases, we can use pytest's parametrize feature.
@pytest.mark.parametrize("num1, num2, expected",[
    (1, 2, 3),
    (2, 3, 5),
    (3, 4, 7),
    (5, 5, 10),
    (10, 20, 30)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_set_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)    # Set initial balance to 50
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit():
    bank_account = BankAccount(50)    # Set initial balance to 50
    bank_account.deposit(60)
    assert bank_account.balance == 110

def test_collect_interest():
    bank_account = BankAccount(50)    # Set initial balance to 50
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
# We did round(bank_account.balance, 6) because the result of the multiplication (50*1.1) is a float and we want to compare it with an int.




# So we can see in the above tests we are using bank_account = BankAccount(50) repeatedly. 
# So we can use the fixture we created above to avoid repeating the same code in multiple tests.
# We can use the fixture by adding it as a parameter to the test function.

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(300)
    zero_bank_account.withdraw(200)
    assert zero_bank_account.balance == 100

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)

])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

