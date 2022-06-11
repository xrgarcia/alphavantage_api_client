import pytest
from .mock_client import MockAlphavantageClient
import json


@pytest.mark.unit
def test_quote_latest_stock_price():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_latest_stock_price(event)

    assert results.success, "Success field is missing or False"
    assert not results.limit_reached, "Limit reached is true but not hitting API"
    assert results.symbol is event["symbol"], "Symbol from results don't match event"
    assert len(results.data), "Global Quote field is missing values"

    print(f"Successfully tested get_latest_stock_price for {event['symbol']}")


@pytest.mark.unit
def test_quote_stock_price():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_stock_price(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["Meta Data"]) > 0, "Meta Data field is zero or not present"
    assert len(results["Time Series (5min)"]) > 0, "Time Series (5min) field is zero or not present"
    print(f"Successfully tested test_quote_stock_price for {event['symbol']}")


@pytest.mark.unit
def test_get_cash_flow():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_cash_flow(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["annualReports"]) > 0, "annualReports field is zero or not present"
    assert len(results["quarterlyReports"]) > 0, "quarterlyReports field is zero or not present"
    print(f"Successfully tested test_get_cash_flow for {event['symbol']}")


@pytest.mark.unit
def test_company_overview():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_company_overview(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["ExDividendDate"]), "ExDividendDate is missing or empty or None"
    assert len(results["Name"]), "Name field is missing or empty or None"
    print(f"Successfully tested test_company_overview for {event['symbol']}")


@pytest.mark.unit
def test_quote_crypto():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ETH",
        "function": "CRYPTO_INTRADAY",
        "outputsize": "full"
    }
    results = client.get_data_from_alpha_vantage(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    print(f"Successfully tested test_quote_crypto for {event['symbol']}")


@pytest.mark.unit
def test_query_earnings():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_earnings(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["annualEarnings"]), "annualEarnings field is missing, empty or None"
    assert len(results["quarterlyEarnings"]), "quarterlyEarnings field is missing, empty or None"
    print(f"Successfully tested test_query_earnings for {event['symbol']}")


@pytest.mark.unit
def test_query_income_statement():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    results = client.get_income_statement_for_symbol(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["annualReports"]), "annualReports field is missing, empty or None"
    assert len(results["quarterlyReports"]), "quarterlyReports field is missing, empty or None"
    print(f"Successfully tested test_query_income_statement for {event['symbol']}")


@pytest.mark.unit
def test_query_real_gdp():
    client = MockAlphavantageClient()
    event = {
        "function": "REAL_GDP",

    }
    results = client.get_data_from_alpha_vantage(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert len(results["unit"]), "unit field is missing, empty or None"
    assert len(results["data"]), "data field is missing, empty or None"
    print(f"Successfully tested test_query_real_gdp")


@pytest.mark.unit
def test_query_technical_indicator_sma():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm",
        "function" : "SMA"
    }
    results = client.get_data_from_alpha_vantage(event)
    assert results.get("success"), "Success field is missing or False"
    assert not results.get("limit_reached"), "Limit reached is true but not hitting API"
    assert results["symbol"] == event["symbol"], "Symbol from results don't match event"
    assert len(results["Meta Data"]), "Meta Data field is missing, empty or None"
    assert len(results["Technical Analysis: SMA"]), "Technical Analysis: SMA field is missing, empty or None"
    print(f"Successfully tested test_query_technical_indicator_sma for {event['symbol']}")