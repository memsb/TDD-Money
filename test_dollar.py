import unittest
from dollar import Money, Bank


class TestMoney(unittest.TestCase):
    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_euros_multiplication(self):
        five = Money.euro(5)
        self.assertEqual(Money.euro(10), five.times(2))
        self.assertEqual(Money.euro(15), five.times(3))

    def test_equality(self):
        self.assertEqual(Money.dollar(5), Money.dollar(5))
        self.assertNotEqual(Money.dollar(5), Money.dollar(6))
        self.assertEqual(Money.euro(5), Money.euro(5))
        self.assertNotEqual(Money.euro(5), Money.euro(6))

        self.assertNotEqual(Money.euro(5), Money.dollar(5))

    def test_currency(self):
        self.assertEqual('USD', Money.dollar(1).currency)
        self.assertEqual('EUR', Money.euro(1).currency)

    def test_addition(self):
        five = Money.dollar(5)
        addition = five.plus(five)

        self.assertEqual(five, addition.left)
        self.assertEqual(five, addition.right)
        bank = Bank()
        reduced = bank.reduce(addition, "USD")
        self.assertEqual(Money.dollar(10), reduced)

    def test_money_reduce(self):
        bank = Bank()
        reduced = bank.reduce(Money.dollar(1), "USD")
        self.assertEqual(Money.dollar(1), reduced)

    def test_reduce_money_to_different_currency(self):
        bank = Bank()
        bank.add_rate("EUR", "USD", 2)
        result = bank.reduce(Money.euro(2), "USD")
        self.assertEqual(Money.dollar(1), result)

    def test_mixed_currency_addition(self):
        five_dollars = Money.dollar(5)
        ten_euros = Money.euro(10)
        bank = Bank()
        bank.add_rate("EUR", "USD", 2)
        expression = five_dollars.plus(ten_euros)
        result = bank.reduce(expression, "USD")
        self.assertEqual(Money.dollar(10), result)

    def test_mixed_currency_multiple_addition(self):
        five_dollars = Money.dollar(5)
        ten_euros = Money.euro(10)
        bank = Bank()
        bank.add_rate("EUR", "USD", 2)
        expression = five_dollars.plus(ten_euros).plus(five_dollars)
        result = bank.reduce(expression, "USD")
        self.assertEqual(Money.dollar(15), result)

    def test_mixed_currency_multiplication(self):
        five_dollars = Money.dollar(5)
        ten_euros = Money.euro(10)
        bank = Bank()
        bank.add_rate("EUR", "USD", 2)
        expression = five_dollars.plus(ten_euros).times(3)
        result = bank.reduce(expression, "USD")
        self.assertEqual(Money.dollar(30), result)


if __name__ == '__main__':
    unittest.main()
