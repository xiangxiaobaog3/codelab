class Custom(object):

    """A customer of ABC Bank with a checking account."""

    def __init__(self, name, balance=0.0):
        """

        :name: @todo
        :balance: @todo

        """
        self._name = name
        self._balance = balance

    def withdraw(self, amount):
        """@todo: Docstring for withdraw.

        :amount: @todo
        :returns: @todo

        """
        if amount > self._balance:
            raise RuntimeError("Amount greater than available balance.")
        self._balance -= amount
        return self._balance

    def deposit(self, amount):
        self._balance += amount
        return self._balance


from abc import ABCMeta, abstractmethod

class Vehicle(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def vehicle_type():
        pass


class Car(Vehicle):
    def vehicle_type(self):
        return 'car'

print(Car().vehicle_type())
