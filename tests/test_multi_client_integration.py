import pytest
import time
from alphavantage_api_client import AlphavantageClient, CsvNotSupported
import logging
import json


# https://intellij-support.jetbrains.com/hc/en-us/community/posts/360000218290-Configure-google-docstring
# above is reference for setting google docstring in pycharm
def setup_function(function):
    pass


def teardown_function(function):
    pass


def setup_module(module):
    pass


def teardown_module(module):
    pass


@pytest.mark.integration
def test_can_query_from_cache():
    event = {
        "symbol": "tsla"
    }
    client = AlphavantageClient().use_simple_cache()

    for i in range(200):
        global_quote = client.get_global_quote(event)
        assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.data) > 0, "Response should have data but contains zero"

    logging.warning(f" Can quote stock symbol in JSON using cache: {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_get_global_quote_json():
    event = {
        "symbol": "tsla"
    }
    client = AlphavantageClient().should_retry_once()

    global_quote = client.get_global_quote(event)
    assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert len(global_quote.data) > 0, "Response should have data but contains zero"
    logging.warning(f" Can quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_get_global_quote_json():
    event = {
        "symbol": "tsla2"
    }
    client = AlphavantageClient().should_retry_once()

    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert not len(global_quote.data), "Response should have data but contains zero"
    logging.warning(f" Can Not quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_get_global_quote_csv():
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    client = AlphavantageClient().should_retry_once()
    global_quote = client.get_global_quote(event)
    assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert len(global_quote.csv) > 0, "Response should have data but contains zero"
    logging.warning(f" Can quote stock symbol in CSV {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_global_quote_wrong_symbol_json():
    event = {
        "symbol": "tsla2323"
    }
    client = AlphavantageClient().should_retry_once()
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    # assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert not len(global_quote.data), "Response should have data but contains zero"
    logging.warning(f" Can NOT quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_global_quote_wrong_symbol_csv():
    event = {
        "symbol": "tsla2233",
        "datatype": "csv"
    }
    client = AlphavantageClient().should_retry_once()
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success: {global_quote.success}, msg: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    # assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert global_quote.csv is None, "Response should have data but contains zero"
    logging.warning(f" Can NOT quote stock symbol in csv {event.get('symbol', None)} : {global_quote.error_message}")


@pytest.mark.limit
def test_can_reach_limit_json():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }
    limit_reached = False
    results = None
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    for i in range(20):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
    logging.warning(f" Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")


@pytest.mark.limit
def test_can_reach_limit_csv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    limit_reached = False
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    results = None
    for i in range(20):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"

    logging.warning(f" Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")


@pytest.mark.integration
def test_can_quote_intraday():
    event = {
        "symbol": "TSLA",
        "interval": "5min"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_intraday_quote(event)
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")


@pytest.mark.integration_paid
def test_can_quote_daily():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_daily_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration
def test_can_quote_daily_adjusted():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_daily_adjusted_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration
def test_can_quote_weekly():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_weekly_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration
def test_can_quote_weekly_adjusted():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_weekly_adjusted_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration
def test_can_quote_monthly():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_monthly_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration
def test_can_quote_monthly_adjusted():
    event = {
        "symbol": "VZ"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_monthly_adjusted_quote(event)
    # print(quote.json())
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration_paid
def test_can_quote_crypto():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min"
    }
    client = AlphavantageClient().should_retry_once()
    quote = client.get_crypto_intraday(event)
    assert not quote.limit_reached, f"limit_reached should not be true {quote.error_message}"
    assert quote.success, f"success is false {quote.error_message}"
    assert len(quote.data), "Data{} property is empty but should have information"
    logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")


@pytest.mark.integration_paid
def test_can_quote_crypto_csv():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min",
        "datatype": "csv"
    }
    client = AlphavantageClient().should_retry_once()
    results = client.get_crypto_intraday(event)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    assert len(results.csv), "Data{} property is empty but should have information"
    logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")


@pytest.mark.integration
def test_can_quote_real_gdp():
    client = AlphavantageClient().should_retry_once()
    real_gdp = client.get_real_gdp()
    assert not real_gdp.limit_reached, f"limit_reached is not present in results {real_gdp.error_message}"
    assert real_gdp.success, f"Success=False but expected true  {real_gdp.error_message}"
    assert len(real_gdp.data), "Data{} is empty but expected results"
    logging.warning(" Can quote Real GDP")


@pytest.mark.integration
def test_can_quote_real_csv():
    event = {
        "function": "REAL_GDP",
        "interval": "annual",
        "datatype": "csv"
    }
    client = AlphavantageClient().should_retry_once()
    real_gdp = client.get_real_gdp(event)
    assert not real_gdp.limit_reached, f"limit_reached is not present in results {real_gdp.error_message}"
    assert real_gdp.success, f"Success=False but expected true  {real_gdp.error_message}"
    assert real_gdp.data is None, "Data{} is empty but expected results"
    assert len(real_gdp.csv), "CSV data is not present"
    logging.warning(" Can quote Real GDP")


@pytest.mark.integration
def test_can_quote_technical_indicator():
    event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open"
    }
    client = AlphavantageClient().should_retry_once()
    technical_indicator = client.get_technical_indicator(event)
    assert not technical_indicator.limit_reached, f"limit_reached is True {technical_indicator.error_message}"
    assert technical_indicator.success, f"Success is False {technical_indicator.error_message}"
    logging.warning(" Can quote IBM EMA technical indicator")


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
    client = AlphavantageClient().should_retry_once()
    technical_indicator = client.get_technical_indicator(event)
    assert not technical_indicator.limit_reached, f"limit_reached is True {technical_indicator.error_message}"
    assert technical_indicator.success, f"Success is False {technical_indicator.error_message}"
    assert len(technical_indicator.csv), "Csv field is empty"
    logging.warning(" Can quote IBM EMA technical indicator")


@pytest.mark.integration
def test_can_query_company_overview():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "TSLA"
    }

    company_overview = client.get_company_overview(event)
    assert company_overview.success, f"Unable to get comapny overview {company_overview.error_message}"
    assert company_overview.symbol == event.get(
        "symbol"), f"Symbols are not equal {company_overview.symbol} : {event.get('symbol')}"
    assert not company_overview.limit_reached, "unexpected limit_reached"
    logging.warning(f" Can query company overview {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_quote_company_overview():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "TSLA2"
    }

    company_overview = client.get_company_overview(event)
    assert not company_overview.success, f"{event.get('symbol')} should not have been successful"
    assert company_overview.symbol != event.get(
        "symbol"), f"Symbols are equal {company_overview.symbol} : {event.get('symbol')} but shouldn't be"
    assert not company_overview.limit_reached, "unexpected limit_reached"
    logging.warning(f" Can not query company overview: {company_overview.error_message}")


@pytest.mark.integration
def test_can_not_query_csv_company_overview():
    with pytest.raises(CsvNotSupported):
        client = AlphavantageClient()
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_company_overview(event)


@pytest.mark.integration
def test_can_not_query_income_statement():
    event = {
        "symbol": "tsla22354q2354"
    }
    client = AlphavantageClient()
    accounting_report = client.get_income_statement(event)
    assert not accounting_report.success, f"success was found to be True: {accounting_report.error_message}"
    assert accounting_report.symbol == event.get("symbol", None), f"Symbols don't match " \
                                                                  f"{accounting_report.symbol} : {event.get('symbol')}"
    logging.warning(f" Can not query  income statement {accounting_report.error_message}")


@pytest.mark.integration
def test_can_query_income_statement():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla"
    }

    accounting_report = client.get_income_statement(event)
    assert accounting_report.success, f"success was found to be false: {accounting_report.error_message}"
    assert not accounting_report.limit_reached, f'{accounting_report.error_message}'
    assert accounting_report.symbol == event.get("symbol", None), f"Symbols don't match " \
                                                                  f"{accounting_report.symbol} : {event.get('symbol')}"
    logging.warning(f" Can query  income statement {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_query_income_statement_csv():
    with pytest.raises(CsvNotSupported):
        client = AlphavantageClient()
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_income_statement(event)


@pytest.mark.integration
def can_query_earnings():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla"
    }

    earnings = client.get_earnings(event)
    assert earnings.success, f"success was found to be false: {earnings.error_message}"
    assert not earnings.limit_reached, f'{earnings.error_message}'
    assert len(earnings.quarterlyReports), "quarterlyReports is empty"
    assert len(earnings.annualReports), "annualReports is empty"
    assert earnings.symbol == event.get("symbol"), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
    logging.warning(f" Can query  earnings {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_query_income_statement():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla"
    }

    income = client.get_income_statement(event)
    assert income.success, f"Unable to get income {income.error_message}"
    assert income.symbol == event.get("symbol"), f"Symbols are not equal {income.symbol} : {event.get('symbol')}"
    assert not income.limit_reached, "limit_reached but should not have"
    logging.warning(f" Can query income statement {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_query_earnings():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla"
    }

    earnings = client.get_earnings(event)
    assert earnings.success, f"success was found to be false: {earnings.error_message}"
    assert not earnings.limit_reached, f"limit_reached is not present in results {earnings.error_message}"
    assert earnings.symbol == event.get("symbol"), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
    logging.warning(f" Can query earnings {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_query_earnings():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla22"
    }

    earnings = client.get_earnings(event)
    assert not earnings.success, f"success was found to be false: {earnings.error_message}"
    assert not earnings.limit_reached, f"limit_reached is not present in results {earnings.error_message}"
    assert earnings.symbol == event.get("symbol"), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
    logging.warning(f" Can not query earnings: {earnings.error_message}")


@pytest.mark.integration
def test_can_not_query_earnings_csv():
    with pytest.raises(CsvNotSupported):
        client = AlphavantageClient()
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_earnings(event)


@pytest.mark.integration
def test_can_query_cash_flow():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla"
    }

    cash_flow = client.get_cash_flow(event)
    assert cash_flow.success, f"success was found to be false: {cash_flow.error_message}"
    assert not cash_flow.limit_reached, f"limit_reached is true {cash_flow.error_message}"
    assert cash_flow.symbol == event.get("symbol"), f"Symbols do not match {cash_flow.symbol} : {event.get('symbol')}"
    assert len(cash_flow.annualReports), "annualReports is empty"
    assert len(cash_flow.quarterlyReports), "quarterlyReports are empty"
    logging.warning(f" Can query  cash flow {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_query_cash_flow():
    client = AlphavantageClient().should_retry_once()
    event = {
        "symbol": "tsla22"
    }

    cash_flow = client.get_cash_flow(event)
    assert not cash_flow.success, f"success was found to be True which is unexpected: {cash_flow.error_message}"
    assert not cash_flow.limit_reached, f"limit_reached is true {cash_flow.error_message}"
    assert cash_flow.symbol == event.get("symbol"), f"Symbols do not match {cash_flow.symbol} : {event.get('symbol')}"
    assert not len(cash_flow.annualReports), "annualReports are not empty"
    assert not len(cash_flow.quarterlyReports), "quarterlyReports are not empty"
    logging.warning(f" Can not query  cash flow {cash_flow.error_message}")


@pytest.mark.integration
def test_can_not_query_cash_flow_csv():
    with pytest.raises(CsvNotSupported):
        client = AlphavantageClient()
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_cash_flow(event)
        logging.warning(f"Querying  cash flow as CSV threw error as expected {event.get('symbol', None)}")


@pytest.mark.integration
def test_get_data_from_alpha_vantage():
    event = {
        "function": "EMA"
    }
    client = AlphavantageClient().should_retry_once()
    results = client.get_data_from_alpha_vantage(event)
    assert type(results) is dict, "Results object should be a dictionary"
    assert len(results) > 0, "There should be data in the results"

    logging.warning("Successfully queried data using get_data_from_alpha_vantage")


@pytest.mark.integration_paid
def test_get_fx_currency_data():
    event = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "JPY",
        "to_currency": "USD"
    }
    client = AlphavantageClient().should_retry_once()
    results = client.get_data_from_alpha_vantage(event)
    # print(results)
    assert results["success"], f"FX Exchange call failed{results}"


@pytest.mark.integration
def test_get_crude_oil_wti():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    crude_wti = client.get_crude_oil_wti_prices(event)
    name = crude_wti.name
    assert crude_wti.success, f"success was found to be False: {crude_wti.error_message}"
    assert not crude_wti.limit_reached, f"limit_reached is true {crude_wti.error_message}"
    assert len(crude_wti.data), f"data is empty, we should have {name} prices"
    assert name == "Crude Oil Prices WTI", f"You are not testing {name}"


@pytest.mark.integration
def test_get_crude_oil_brent():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    crude_brent = client.get_crude_oil_brent_prices(event)
    name = crude_brent.name
    assert crude_brent.success, f"success was found to be False: {crude_brent.error_message}"
    assert not crude_brent.limit_reached, f"limit_reached is true {crude_brent.error_message}"
    assert len(crude_brent.data), f"data is empty, we should have {name} prices"
    assert name == "Crude Oil Prices Brent", f"You are not testing {name}"


@pytest.mark.integration
def test_get_natural_gas():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    natural_gas = client.get_natural_gas_prices(event)
    name = natural_gas.name
    assert natural_gas.success, f"success was found to be False: {natural_gas.error_message}"
    assert not natural_gas.limit_reached, f"limit_reached is true {natural_gas.error_message}"
    assert len(natural_gas.data), f"data is empty, we should have {name} prices"
    assert name == "Henry Hub Natural Gas Spot Price", f"You are not testing {name}"


@pytest.mark.integration
def test_get_copper():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    copper = client.get_copper_prices(event)
    name = copper.name
    assert copper.success, f"success was found to be False: {copper.error_message}"
    assert not copper.limit_reached, f"limit_reached is true {copper.error_message}"
    assert len(copper.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Copper", f"You are not testing {name}"


def test_get_aluminum():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    aluminum = client.get_aluminum_prices(event)
    name = aluminum.name
    assert aluminum.success, f"success was found to be False: {aluminum.error_message}"
    assert not aluminum.limit_reached, f"limit_reached is true {aluminum.error_message}"
    assert len(aluminum.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Aluminum", f"You are not testing {name}"


def test_get_wheat():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    wheat = client.get_wheat_prices(event)
    name = wheat.name
    assert wheat.success, f"success was found to be False: {wheat.error_message}"
    assert not wheat.limit_reached, f"limit_reached is true {wheat.error_message}"
    assert len(wheat.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Wheat", f"You are not testing {name}"


def test_get_corn():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    corn = client.get_corn_prices(event)
    name = corn.name
    assert corn.success, f"success was found to be False: {corn.error_message}"
    assert not corn.limit_reached, f"limit_reached is true {corn.error_message}"
    assert len(corn.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Corn", f"You are not testing {name}"


def test_get_cotton():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    cotton = client.get_cotton_prices(event)
    name = cotton.name
    assert cotton.success, f"success was found to be False: {cotton.error_message}"
    assert not cotton.limit_reached, f"limit_reached is true {cotton.error_message}"
    assert len(cotton.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Cotton", f"You are not testing {name}"


def test_get_sugar():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    sugar = client.get_sugar_prices(event)
    name = sugar.name
    assert sugar.success, f"success was found to be False: {sugar.error_message}"
    assert not sugar.limit_reached, f"limit_reached is true {sugar.error_message}"
    assert len(sugar.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Sugar", f"You are not testing {name}"


@pytest.mark.integration
def test_get_coffee_commodity():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    coffee = client.get_coffee_prices(event)
    name = coffee.name
    assert coffee.success, f"success was found to be False: {coffee.error_message}"
    assert not coffee.limit_reached, f"limit_reached is true {coffee.error_message}"
    assert len(coffee.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price of Coffee", f"You are not testing {name}"


@pytest.mark.integration
def test_get_all_commodities():
    client = AlphavantageClient()
    event = {
        "interval": "daily"
    }
    all_commodities = client.get_all_commodity_prices(event)
    name = all_commodities.name
    assert all_commodities.success, f"success was found to be False: {all_commodities.error_message}"
    assert not all_commodities.limit_reached, f"limit_reached is true {all_commodities.error_message}"
    assert len(all_commodities.data), f"data is empty, we should have {name} prices"
    assert name == "Global Price Index of All Commodities", f"You are not testing {name}"
