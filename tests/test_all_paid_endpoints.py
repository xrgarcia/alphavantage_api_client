import pytest
from .test_base import BaseTestSuite
import time
from alphavantage_api_client import AlphavantageClient, CsvNotSupported, Ticker
import logging


class AllPaidEndPointTests(BaseTestSuite):

    @pytest.mark.integration_paid
    def test_can_quote_daily(self):
        event = {
            "symbol": "VZ"
        }
        daily_quote = self.get_client().get_daily_quote(event)
        assert not daily_quote.limit_reached, f"limit_reached should not be true {daily_quote.error_message}"
        assert daily_quote.success, f"success is false {daily_quote.error_message}"
        assert len(daily_quote.data), f"Did not return data for this symbol {daily_quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration_paid
    def test_get_forex_intraday_rates(self):
        event = {
            "from_symbol": "EUR",
            "to_symbol": "USD"
        }
        currency_quote = self.get_client().get_forex_intraday(event)
        assert currency_quote.success, f"success was found to be True which is unexpected: {currency_quote.error_message}"
        assert not currency_quote.limit_reached, f"limit_reached is true {currency_quote.error_message}"
        assert len(currency_quote.meta_data), "meta_data is not defined within response"
        assert len(currency_quote.data), "data is not defined or zero within response"

    @pytest.mark.integration_paid
    def test_can_quote_crypto_csv(self):
        event = {
            "function": "CRYPTO_INTRADAY",
            "symbol": "ETH",
            "market": "USD",
            "interval": "5min",
            "datatype": "csv"
        }
        results = self.get_client().get_crypto_intraday(event)
        assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
        assert results.success, f"success is false {results.error_message}"
        assert len(results.csv), "Data{} property is empty but should have information"
        logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")

    @pytest.mark.integration_paid
    def test_can_quote_crypto_intraday(self):
        event = {
            "symbol": "ETH",
            "outputsize": "compact"
        }
        quote = self.get_client().get_crypto_intraday(event)
        # print(quote)
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), "Data{} property is empty but should have information"
        logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")

    @pytest.mark.integration_paid
    def test_can_quote_crypto_csv(self):
        event = {
            "symbol": "ETH",
            "datatype": "csv"
        }
        results = self.get_client().get_crypto_intraday(event)
        assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
        assert results.success, f"success is false {results.error_message}"
        assert len(results.csv), "csv property is empty but should have information"
        logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")
