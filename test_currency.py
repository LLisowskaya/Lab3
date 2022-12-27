import unittest
import pytest
from unittest import mock

from currency import get_total_currency_value, get_currency_value_from_api


class TestCurrency(unittest.TestCase):

    @pytest.mark.base
    def test_currency_positive(self):
        res = get_total_currency_value(
            rate='GBP',
            count=100_000,
            discount=100
       )
        self.assertEqual(res, 1219.62)

    @pytest.mark.base
    def test_currency_negative(self):
        with self.assertRaises(ValueError) as err:
            get_total_currency_value('GBP', 100_000, -1)

    @pytest.mark.api
    def test_currency_with_api(self):
        with mock.patch('currency.get_currency_value_from_api') as mock_currency:
            mock_currency.return_value = 0.0131962
            res = get_total_currency_value(
                rate = 'GBP',
                count = 100_000,
                discount=100
            )
            self.assertEqual(res, 1219.62)

@pytest.mark.parametrize("num, output", [(0.0275192, 2651.92), (0.039605, 3860.5), (6.39742056, 639642.056), (0.0275192, 1)])
def test_currency_multiple(num, output):
    assert 100_000*num - 100 == output


@pytest.mark.parametrize("rate, output", [('AUD', 0.02376019), ('GBP', 0.0131962), ('AMD', 6.39742056), ('BYN', 0)])
def test_currency_multiple_rate(rate, output):
    res = get_currency_value_from_api(rate)
    assert res == output

@pytest.mark.parametrize("rate, value, output", [('AUD', 0.02376019, 2276.0190000000002),
                                                 ('GBP', 0.0131962, 1219.62),
                                                 ('AMD', 6.39742056, 639642.056),
                                                 ('BYN', 0, -1)])
def test_currency_multiple_rate_value(rate, value, output):
    res = get_currency_value_from_api(rate)
    assert (res == value) & (100_000 * res - 100 == output)


