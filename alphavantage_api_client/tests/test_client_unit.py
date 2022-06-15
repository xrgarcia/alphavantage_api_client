import pytest
from .mock_client import MockAlphavantageClient
import json


@pytest.mark.unit
def test_get_intraday_quote():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm",
        "interval": "5min"
    }
    intraday_quote = client.get_intraday_quote(event)
    assert intraday_quote.success, "Success field is missing or False"
    assert not intraday_quote.limit_reached, "Limit reached is true but not hitting API"
    assert intraday_quote.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(intraday_quote.meta_data) > 0, "Meta Data field is zero or not present"
    assert len(intraday_quote.data) > 0, "Data field is zero or not present"
    print(f"Successfully tested test_quote_stock_price for {event['symbol']}")


@pytest.mark.unit
def test_get_global_quote():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm",
        "interval": "5min"
    }
    global_quote = client.get_global_quote(event)
    assert global_quote.success, "Success field is missing or False"
    assert not global_quote.limit_reached, "Limit reached is true but not hitting API"
    assert global_quote.symbol == event["symbol"], "Symbol from results don't match event"
    assert "metra_data" not in global_quote, "Metadata should not be present since it's not in the api"
    assert len(global_quote.data) > 0, "Data field is zero or not present"
    print(f"Successfully tested test_quote_stock_price for {event['symbol']}")


@pytest.mark.unit
def test_get_cash_flow():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    accounting_report = client.get_cash_flow(event)
    assert accounting_report.success, "Success field is missing or False"
    assert not accounting_report.limit_reached, "Limit reached is true but not hitting API"
    assert accounting_report.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(accounting_report.annualReports) > 0, "annualReports field is zero or not present"
    assert len(accounting_report.quarterlyReports) > 0, "quarterlyReports field is zero or not present"
    print(f"Successfully tested test_get_cash_flow for {event['symbol']}")


@pytest.mark.unit
def test_company_overview():
    client = MockAlphavantageClient()
    event = {
        "symbol": "IBM"
    }
    company_overview = client.get_company_overview(event)
    assert company_overview.success, "Success field is missing or False"
    assert not company_overview.limit_reached, "Limit reached is true but not hitting API"
    assert company_overview.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(company_overview.ex_dividend_date), "ExDividendDate is missing or empty or None"
    assert len(company_overview.analyst_target_price), "analyst_target_price field is missing or empty or None"
    print(f"Successfully tested test_company_overview for {event['symbol']}")


@pytest.mark.unit
def test_quote_crypto():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ETH",
        "function": "CRYPTO_INTRADAY",
        "outputsize": "full"
    }
    intraday_quote = client.get_crypto_intraday(event)
    assert intraday_quote.success, "Success field is missing or False"
    assert not intraday_quote.limit_reached, "Limit reached is true but not hitting API"
    assert intraday_quote.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(intraday_quote.data), "data{} is empty but it should contain properties"
    assert len(intraday_quote.meta_data), "meta_data{} is empty but it should contain properties"
    print(f"Successfully tested test_quote_crypto for {event['symbol']}")


@pytest.mark.unit
def test_query_earnings():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm"
    }
    accounting_report = client.get_earnings(event)
    assert accounting_report.success, "Success field is missing or False"
    assert not accounting_report.limit_reached, "Limit reached is true but not hitting API"
    assert accounting_report.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(accounting_report.annualReports), "annualEarnings[] field is missing, empty or None"
    assert len(accounting_report.quarterlyReports), "quarterlyEarnings[] field is missing, empty or None"
    print(f"Successfully tested test_query_earnings for {event['symbol']}")


@pytest.mark.unit
def test_query_income_statement():
    client = MockAlphavantageClient()
    event = {
        "symbol": "IBM"
    }
    accounting_report = client.get_income_statement(event)
    assert accounting_report.success, "Success field is missing or False"
    assert not accounting_report.limit_reached, "Limit reached is true but not hitting API"
    assert accounting_report.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(accounting_report.annualReports), "annualReports field is missing, empty or None"
    assert len(accounting_report.quarterlyReports), "quarterlyReports field is missing, empty or None"
    print(f"Successfully tested test_query_income_statement for {event['symbol']}")


@pytest.mark.unit
def test_query_real_gdp():
    client = MockAlphavantageClient()
    event = {
        "function": "REAL_GDP",

    }
    real_gdp = client.get_real_gdp(event)
    assert real_gdp.success, "Success field is missing or False"
    assert not real_gdp.limit_reached, "Limit reached is true but not hitting API"
    assert len(real_gdp.unit), "unit field is missing, empty or None"
    assert len(real_gdp.data), "data field is missing, empty or None"
    print(f"Successfully tested test_query_real_gdp")


@pytest.mark.unit
def test_query_technical_indicator_sma():
    client = MockAlphavantageClient()
    event = {
        "symbol": "ibm",
        "function": "SMA"
    }
    quote = client.get_technical_indicator(event)
    assert quote.success, "Success field is missing or False"
    assert not quote.limit_reached, "Limit reached is true but not hitting API"
    assert quote.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(quote.meta_data), "Meta Data field is missing, empty or None"
    assert len(quote.data), "Technical Analysis: SMA field is missing, empty or None"
    print(f"Successfully tested test_query_technical_indicator_sma for {event['symbol']}")


@pytest.mark.unit
def test_can_convert_to_json_string():
    event = {
        "symbol": "tsla"
    }
    client = MockAlphavantageClient()
    global_quote = client.get_global_quote(event)
    print(global_quote.json())


@pytest.mark.unit
def test_can_get_data_from_alpha_vantage():
    event = {
        "function": "EMA"
    }
    client = MockAlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert type(results) is dict, "Results object should be a dictionary"
    assert len(results) > 0, "There should be data in the results"

    print("Successfully queried data using get_data_from_alpha_vantage")
