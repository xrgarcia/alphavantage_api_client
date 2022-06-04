import pytest
import json
import os
from alphavantage_api_client import AlphavantageClient


def setup_function(function):
    pass


def teardown_function(function):
    pass


def setup_module(module):
    pass


def teardown_module(module):
    pass


def quoteLatestPrice(success_criteria=True, event=None):
    assert event != None
    client = AlphavantageClient()

    try:
        latest_stock_price = client.get_latest_stock_price(event)
    except ValueError as error:
        assert error == None, error
    assert "limit" not in latest_stock_price, f"{latest_stock_price['Error Message']}"
    assert len(latest_stock_price) > 0, "Response should have fields but contains zero"
    assert latest_stock_price[
               'success'] == success_criteria, f"success was found to be false: {latest_stock_price['Error Message']}"
    assert "symbol" in latest_stock_price, "Symbol field not present in response"
    assert latest_stock_price["symbol"] == event[
        "symbol"], f"Symbol {latest_stock_price['symbol']} is not equal to {event['symbol']}"

    return latest_stock_price


def test_canQuoteStockSymbol():
    event = {
        "symbol": "tsla"
    }
    quoteLatestPrice(True, event)
    print(f"Can quote stock symbol {event['symbol']}")


def test_canNotQuoteWrongSymbol():
    event = {
        "symbol": "tsla2233"
    }
    quoteLatestPrice(False, event)
    print(f"Can NOT quote stock symbol {event['symbol']}")


def test_canReachLimit():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }
    limit_reached = False
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    for i in range(7):
        latest_stock_price = client.get_latest_stock_price(event)
        # print(json.dumps(latest_stock_price))
        if "limit_reached" in latest_stock_price:
            limit_reached = latest_stock_price["limit_reached"]
        if limit_reached == True:
            break

    assert limit_reached == True, "Did NOT reached Limit as expected"
    assert "symbol" in latest_stock_price, "symbol field NOT present in response"
    assert latest_stock_price["symbol"] == event["symbol"], f"Did not find {event['symbol']} in response"
    print(f"Can Reach Limit while quoting for symbol {event['symbol']}")
