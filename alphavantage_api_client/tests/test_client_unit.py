import pytest
from .mock_client import MockAlphavantageClient
import json


@pytest.mark.unit
def test_quote_latest_stock_price():
    client = MockAlphavantageClient()
    event = {
        "symbol": "tsla"
    }
    results = client.get_latest_stock_price(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"],"Symbol from results don't match event"
    print(f"Successfully tested get_latest_stock_price for {event['symbol']}")
