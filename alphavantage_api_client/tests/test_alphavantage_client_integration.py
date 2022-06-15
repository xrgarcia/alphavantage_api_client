import pytest
import json
import os
import time
from alphavantage_api_client import AlphavantageClient
from alphavantage_api_client.models.core import CsvNotSupported


def setup_function(function):
    pass


def teardown_function(function):
    pass


def setup_module(module):
    pass


def teardown_module(module):
    pass


@pytest.mark.integration
def test_can_get_global_quote_json():
    event = {
        "symbol": "tsla"
    }
    client = AlphavantageClient()

    global_quote = client.get_global_quote(event)
    assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert len(global_quote.data) > 0, "Response should have data but contains zero"
    print(f" Can quote stock symbol in JSON {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_get_global_quote_csv():
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    global_quote = client.get_global_quote(event)
    assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert len(global_quote.csv) > 0, "Response should have data but contains zero"
    print(f" Can quote stock symbol in CSV {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotGlobalQuoteWrongSymbolJson():
    event = {
        "symbol": "tsla2323"
    }
    client = AlphavantageClient()
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert not len(global_quote.data), "Response should have data but contains zero"
    print(f" Can NOT quote stock symbol in JSON {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotGlobalQuoteWrongSymbolCsv():
    event = {
        "symbol": "tsla2233",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert global_quote.csv is None, "Response should have data but contains zero"
    print(f" Can NOT quote stock symbol in csv {event.get('symbol', None)} : {global_quote.error_message}")
    time.sleep(20)


@pytest.mark.integration
def test_canReachLimitJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }
    limit_reached = False
    results = None
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    for i in range(7):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
    print(f" Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")
    time.sleep(60)


@pytest.mark.integration
def test_canReachLimitCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    limit_reached = False
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    results = None
    for i in range(7):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"

    print(f" Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")
    time.sleep(60)


@pytest.mark.integration
def test_can_quote_intraday():
    event = {
        "symbol": "TSLA",
        "interval": "5min"
    }
    client = AlphavantageClient()
    intra_day_quote = client.get_intraday_quote(event)
    assert not intra_day_quote.limit_reached, f"limit_reached should not be true {intra_day_quote.error_message}"
    assert intra_day_quote.success, f"success is false {intra_day_quote.error_message}"
    assert len(intra_day_quote.data), f"Did not return data for this symbol {intra_day_quote.symbol}"
    print(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_crypto():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min"
    }
    client = AlphavantageClient()
    results = client.get_crypto_intraday(event)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    assert len(results.data), "Data{} property is empty but should have information"
    print(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_crypto_csv():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    results = client.get_crypto_intraday(event)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    assert len(results.csv), "Data{} property is empty but should have information"
    print(f" Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_real_gdp():
    event = {
        "function": "REAL_GDP",
        "interval": "annual"
    }
    client = AlphavantageClient()
    real_gdp = client.get_real_gdp(event)
    assert not real_gdp.limit_reached, f"limit_reached is not present in results {real_gdp.error_message}"
    assert real_gdp.success, f"Success=False but expected true  {real_gdp.error_message}"
    assert len(real_gdp.data), "Data{} is empty but expected results"
    print(" Can quote Real GDP")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_real_csv():
    event = {
        "function": "REAL_GDP",
        "interval": "annual",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    real_gdp = client.get_real_gdp(event)
    assert not real_gdp.limit_reached, f"limit_reached is not present in results {real_gdp.error_message}"
    assert real_gdp.success, f"Success=False but expected true  {real_gdp.error_message}"
    assert real_gdp.data is None, "Data{} is empty but expected results"
    assert len(real_gdp.csv), "CSV data is not present"
    print(" Can quote Real GDP")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_technical_indicator():
    event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open"
    }
    client = AlphavantageClient()
    technical_indicator = client.get_technical_indicator(event)
    assert not technical_indicator.limit_reached, f"limit_reached is True {technical_indicator.error_message}"
    assert technical_indicator.success, f"Success is False {technical_indicator.error_message}"
    print(" Can quote IBM EMA technical indicator")
    time.sleep(20)


@pytest.mark.integration
def test_can_quote_technical_indicator_csv():
    event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    technical_indicator = client.get_technical_indicator(event)
    assert not technical_indicator.limit_reached, f"limit_reached is True {technical_indicator.error_message}"
    assert technical_indicator.success, f"Success is False {technical_indicator.error_message}"
    assert len(technical_indicator.csv), "Csv field is empty"
    print(" Can quote IBM EMA technical indicator")
    time.sleep(20)


@pytest.mark.integration
def test_can_query_company_overview():
    client = AlphavantageClient()
    event = {
        "symbol": "TSLA"
    }

    company_overview = client.get_company_overview(event)
    assert company_overview.success, f"Unable to get comapny overview {company_overview.error_message}"
    assert company_overview.symbol == event.get(
        "symbol"), f"Symbols are not equal {company_overview.symbol} : {event.get('symbol')}"
    assert not company_overview.limit_reached, "unexpected limit_reached"
    print(f" Can query company overview {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_company_overview():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_company_overview(event)
        assert True == False, "Expected an error because company overview doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because company overview doesn't support csv"

    print(f" Querying Company Overview as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_query_income_statement():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    accounting_report = client.get_income_statement(event)
    assert accounting_report.success, f"success was found to be false: {accounting_report.error_message}"
    assert accounting_report.limit_reached == False, f'{accounting_report.error_message}'
    assert accounting_report.symbol == event.get("symbol", None), f"Symbols don't match " \
                                                                  f"{accounting_report.symbol} : {event.get('symbol')}"
    print(f" Can query latest income statement {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_income_statement_csv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_income_statement(event)
        assert True == False, "Expected an error because latest income statement doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because latest income statement doesn't support csv"

    print(f" Querying latest income statement as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def can_query_earnings():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    earnings = client.get_earnings(event)
    assert earnings.success, f"success was found to be false: {earnings.error_message}"
    assert not earnings.limit_reached, f'{earnings.error_message}'
    assert len(earnings.quarterlyReports), "quarterlyReports is empty"
    assert len(earnings.annualReports), "annualReports is empty"
    assert earnings.symbol == event.get("symbol"), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
    print(f" Can query latest earnings {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_earnings():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_earnings(event)
        assert True == False, "Expected an error because get_earnings doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because get_earnings doesn't support csv"

    print(f" Querying earnings as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_query_income_statement():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    income = client.get_income_statement(event)
    assert income.success, f"Unable to get income {income.error_message}"
    assert income.symbol == event.get("symbol"), f"Symbols are not equal {income.symbol} : {event.get('symbol')}"
    assert not income.limit_reached, "limit_reached but should not have"
    print(f" Can query income statement {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_income_statement():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_income_statement(event)
        assert True == False, "Expected an error because income statement doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because income statement doesn't support csv"

    print(f" Querying income statement as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_query_earnings():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    earnings = client.get_earnings(event)
    assert earnings.success, f"success was found to be false: {earnings.error_message}"
    assert not earnings.limit_reached, f"limit_reached is not present in results {earnings.error_message}"
    assert earnings.symbol == event.get("symbol"), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
    print(f" Can query earnings {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_earnings_csv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_earnings(event)
        assert True == False, "Expected an error because earnings doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because earnings doesn't support csv"

    print(f" Querying earnings as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_query_cash_flow():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    cash_flow = client.get_cash_flow(event)
    assert cash_flow.success, f"success was found to be false: {cash_flow.error_message}"
    assert not cash_flow.limit_reached, f"limit_reached is true {cash_flow.error_message}"
    assert cash_flow.symbol == event.get("symbol"), f"Symbols do not match {cash_flow.symbol} : {event.get('symbol')}"
    assert len(cash_flow.annualReports), "annualReports is empty"
    assert len(cash_flow.quarterlyReports), "quarterlyReports are empty"
    print(f" Can query latest cash flow {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_can_not_query_cash_flow_csv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_cash_flow(event)
        assert True == False, "Expected an error because latest cash flow doesn't support csv"
    except CsvNotSupported as error:
        assert True == True, "Expected an error because latest cash flow doesn't support csv"

    print(f" Querying latest cash flow as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.unit
def test_get_data_from_alpha_vantage():
    event = {
        "function": "EMA"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert type(results) is dict, "Results object should be a dictionary"
    assert len(results) > 0, "There should be data in the results"

    print("Successfully queried data using get_data_from_alpha_vantage")
    time.sleep(20)