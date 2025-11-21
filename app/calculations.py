def add(digit1: int, digit2: int) -> int:
    return digit1 + digit2

def subtract(digit1: int, digit2: int) -> int:
    return digit1 - digit2  

def multiply(digit1: int, digit2: int) -> int:
    return digit1 * digit2  

def divide(digit1: int, digit2: int) -> float:
    if digit2 == 0:
        raise ValueError("Cannot divide by zero.")
    return digit1 / digit2      

def power(base: int, exponent: int) -> int:
    return base ** exponent     

def modulus(digit1: int, digit2: int) -> int:
    return digit1 % digit2  

class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1 