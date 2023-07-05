from alphavantage_api_client import AlphavantageClient
from .test_all_free_endpoints import AllEndPointTests
from .test_base import BaseTestSuite
import pytest
import logging

class TestMultiClientLimitReached(BaseTestSuite):

    def setup_class(cls):
        # turn retry off so we can hit limit
        cls.__client__ = AlphavantageClient()

    def get_client(self) -> AlphavantageClient:
        return self.__client__

    @pytest.mark.limit
    def test_canReachLimitJson(self):
        symbols = ["VZ", "PATH", "ZM", "TSLA", "AAPL", "GOOG", "C", "VICI", "TDOC", "ALLY", "AMZN", "MSFT", "NLY"]
        limit_reached = False
        results = None
        for index, symbol in enumerate(symbols):
            event = {
                "symbol": symbol
            }
            results = self.get_client().get_global_quote(event)
            if results.limit_reached:
                limit_reached = True
                break

        assert limit_reached, "Failed to reach limit"
        assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
        logging.warning(f" Can Reach Limit while quoting for symbols {symbols}")

    @pytest.mark.limit
    def test_canReachLimitCsv(self):
        symbols = ["VZ", "PATH", "ZM", "TSLA", "AAPL", "GOOG", "C", "VICI", "TDOC", "ALLY", "AMZN", "MSFT", "NLY"]
        limit_reached = False
        results = None
        for index, symbol in enumerate(symbols):
            event = {
                "symbol": symbol,
                "datatype": "csv"
            }
            results = self.get_client().get_global_quote(event)
            if results.limit_reached:
                limit_reached = True
                break

        assert limit_reached, "Failed to reach limit"
        assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"

        logging.warning(f" Can Reach Limit while quoting for symbols {symbols}")
