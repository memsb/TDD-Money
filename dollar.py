class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        return other.currency == self.currency and other.amount == self.amount

    def times(self, multiplier):
        return self.__class__(self.amount * multiplier, self.currency)

    def plus(self, money):
        return Addition(self, money)

    @staticmethod
    def dollar(amount):
        return Money(amount, "USD")

    @staticmethod
    def euro(amount):
        return Money(amount, "EUR")

    def reduce(self, bank, currency):
        rate = bank.rate(self.currency, currency)
        return Money(self.amount / rate, currency)


class Addition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def plus(self, expression):
        return Addition(self, expression)

    def times(self, multiplier):
        return Addition(self.left.times(multiplier), self.right.times(multiplier))

    def reduce(self, bank, currency):
        left = self.left.reduce(bank, currency)
        right = self.right.reduce(bank, currency)
        amount = left.amount + right.amount
        return Money(amount, currency)


class Bank:

    def __init__(self):
        self.rates = {}

    def add_rate(self, origin, destination, rate):
        self.rates[f"{origin}_{destination}"] = rate
        self.rates[f"{destination}_{origin}"] = 1 / rate

    def rate(self, origin, destination):
        if origin == destination:
            return 1
        return self.rates[f"{origin}_{destination}"]

    def reduce(self, expression, currency):
        return expression.reduce(self, currency)
