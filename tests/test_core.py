import pytest
from .test_base import BaseTestSuite
import time
from alphavantage_api_client import AlphavantageClient, CsvNotSupported
import logging
import json
from abc import ABC, abstractmethod


class CoreApiEndPointTests(BaseTestSuite):

    @pytest.mark.integration
    def test_can_get_global_quote_json(self):
        event = {
            "symbol": "tsla"
        }

        global_quote = self.get_client().get_global_quote(event)
        assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.data) > 0, "Response should have data but contains zero"
        logging.warning(f" Can quote stock symbol in JSON {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_not_get_global_quote_json(self):
        event = {
            "symbol": "tsla2"
        }

        global_quote = self.get_client().get_global_quote(event)
        assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(f" Can Not quote stock symbol in JSON {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_get_global_quote_csv(self):
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        global_quote = self.get_client().get_global_quote(event)
        assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.csv) > 0, "Response should have data but contains zero"
        logging.warning(f" Can quote stock symbol in CSV {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_not_global_quote_wrong_symbol_json(self):
        event = {
            "symbol": "tsla2323"
        }
        global_quote = self.get_client().get_global_quote(event)
        assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(f" Can NOT quote stock symbol in JSON {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_not_global_quote_wrong_symbol_csv(self):
        event = {
            "symbol": "tsla2233",
            "datatype": "csv"
        }
        global_quote = self.get_client().get_global_quote(event)
        assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert global_quote.csv is None, "Response should have data but contains zero"
        logging.warning(
            f" Can NOT quote stock symbol in csv {event.get('symbol', None)} : {global_quote.error_message}")

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

    @pytest.mark.integration
    def test_can_quote_intraday(self):
        event = {
            "symbol": "TSLA",
            "interval": "5min"
        }
        quote = self.get_client().get_intraday_quote(event)
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_daily_adjusted(self):
        event = {
            "symbol": "VZ"
        }
        quote = self.get_client().get_daily_adjusted_quote(event)
        # print(quote.json())
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly(self):
        event = {
            "symbol": "VZ"
        }
        quote = self.get_client().get_weekly_quote(event)
        # print(quote.json())
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly_adjusted(self):
        event = {
            "symbol": "VZ"
        }
        quote = self.get_client().get_weekly_adjusted_quote(event)
        # print(quote.json())
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_monthly(self):
        event = {
            "symbol": "VZ"
        }
        quote = self.get_client().get_monthly_quote(event)
        # print(quote.json())
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_monthly_adjusted(self):
        event = {
            "symbol": "VZ"
        }
        quote = self.get_client().get_monthly_adjusted_quote(event)
        # print(quote.json())
        assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_get_most_recent_intraday(self):
        symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
        for symbol in symbols:
            event = {
                "symbol": symbol
            }
            latest_quote = self.get_client().get_intraday_quote(event).get_most_recent_value()
            print(symbol, latest_quote)

        metrics = self.get_client().get_internal_metrics()
        #print(metrics)

    @pytest.mark.integration
    def test_get_intraday_with_params(self):
        symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
        for symbol in symbols:
            event = {
                "symbol": symbol,
                "adjusted": False,
                "interval": "60min"
            }
            intraday_quote = self.get_client().get_intraday_quote(event)
            assert event["interval"] == intraday_quote.meta_data["4. Interval"], \
                f"The interval doesn't match, {event['interval']} != {intraday_quote.meta_data['4. Interval']}"

    @pytest.mark.integration
    def test_get_daily_quote_with_params(self):
        symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
        for symbol in symbols:
            event = {
                "adjusted": False,
                "outputsize": "compact",
                "symbol": symbol
            }
            daily_quote = self.get_client().get_daily_quote(event)
            expected_output_size = event["outputsize"].upper()
            given_output_size = None
            if "4. Output Size" in daily_quote.meta_data:
                given_output_size = daily_quote.meta_data["4. Output Size"].upper()
            assert expected_output_size == given_output_size, \
                f"The interval doesn't match, {expected_output_size} != {given_output_size}"

    @pytest.mark.integration
    def test_can_search_ticker(self):
        event = {
            "keywords": "Tesla"
        }
        ticker_search_result = self.get_client().search_ticker(event)
        assert not ticker_search_result.limit_reached, f"limit_reached should not be true {ticker_search_result.error_message}"
        assert ticker_search_result.success, f"success is false {ticker_search_result.error_message}"
        assert len(ticker_search_result.data), f"Did not return bestMatches for this search {event['keywords']}"
        for result in ticker_search_result.data:
            assert "9. matchScore" in result, f"9. matchScore property is not in search result for {event['keywords']}"
            assert "1. symbol" in result, f"1. symbol property is not in search result for {event['keywords']}"
            assert "2. name" in result, f"2. name property is not in search result for {event['keywords']}"
            assert "3. type" in result, f"3. type property is not in search result for {event['keywords']}"
