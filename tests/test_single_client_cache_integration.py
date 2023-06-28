import pytest
import time
from alphavantage_api_client import AlphavantageClient, CsvNotSupported, TickerSearch, MarketStatus, MarketMovers\
    , NewsAndSentiment
import logging
import json
import csv
client = AlphavantageClient().should_retry_once().use_simple_cache()


@pytest.mark.integration
def test_can_get_news_and_sentiment():
    event = {
        "function" : "NEWS_SENTIMENT",
        "tickers": "TSLA"
    }
    result = client.get_data_from_alpha_vantage(event)
    print(json.dumps(result))
    assert result['success'], 'could not get news and sentiment'

@pytest.mark.integration
def test_can_query_from_cache():
    event = {
        "symbol": "tsla"
    }

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
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert not len(global_quote.data), "Response should have data but contains zero"
    logging.warning(f" Can NOT quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_can_not_global_quote_wrong_symbol_csv():
    event = {
        "symbol": "tsla2233",
        "datatype": "csv"
    }
    global_quote = client.get_global_quote(event)
    assert not global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert global_quote.csv is None, "Response should have data but contains zero"
    logging.warning(f" Can NOT quote stock symbol in csv {event.get('symbol', None)} : {global_quote.error_message}")


@pytest.mark.limit
def test_canReachLimitJson():
    symbols = ["VZ", "PATH", "ZM", "TSLA", "AAPL", "GOOG", "C", "VICI", "TDOC", "ALLY", "AMZN", "MSFT", "NLY"]
    limit_reached = False
    results = None
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    client.clear_cache().should_retry_once(False)  # turn retry off so we can hit limit
    for index, symbol in enumerate(symbols):
        event = {
            "symbol": symbol
        }
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break
    client.should_retry_once()  # turn retry back on
    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
    logging.warning(f" Can Reach Limit while quoting for symbols {symbols}")


@pytest.mark.limit
def test_canReachLimitCsv():
    symbols = ["VZ", "PATH", "ZM", "TSLA", "AAPL", "GOOG", "C", "VICI", "TDOC", "ALLY", "AMZN", "MSFT", "NLY"]
    limit_reached = False
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    results = None
    client.clear_cache().should_retry_once(False)  # turn retry off so we can hit limit
    for index, symbol in enumerate(symbols):
        event = {
            "symbol": symbol,
            "datatype": "csv"
        }
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    client.should_retry_once()  # turn retry back on
    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"

    logging.warning(f" Can Reach Limit while quoting for symbols {symbols}")


@pytest.mark.integration
def test_can_quote_intraday():
    event = {
        "symbol": "TSLA",
        "interval": "5min"
    }
    intra_day_quote = client.get_intraday_quote(event)
    assert not intra_day_quote.limit_reached, f"limit_reached should not be true {intra_day_quote.error_message}"
    assert intra_day_quote.success, f"success is false {intra_day_quote.error_message}"
    assert len(intra_day_quote.data), f"Did not return data for this symbol {intra_day_quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

@pytest.mark.integration
def test_can_search_ticker():
    event = {
        "keywords" : "Tesla"
    }
    ticker_search_result = client.search_ticker(event)
    assert not ticker_search_result.limit_reached, f"limit_reached should not be true {ticker_search_result.error_message}"
    assert ticker_search_result.success, f"success is false {ticker_search_result.error_message}"
    assert len(ticker_search_result.data), f"Did not return bestMatches for this search {event['keywords']}"
    for result in ticker_search_result.data:
        assert "9. matchScore" in result, f"9. matchScore property is not in search result for {event['keywords']}"
        assert "1. symbol" in result, f"1. symbol property is not in search result for {event['keywords']}"
        assert "2. name" in result, f"2. name property is not in search result for {event['keywords']}"
        assert "3. type" in result, f"3. type property is not in search result for {event['keywords']}"


@pytest.mark.integration_paid
def test_can_quote_daily():
    event = {
        "symbol": "VZ"
    }
    daily_quote = client.get_daily_quote(event)
    assert not daily_quote.limit_reached, f"limit_reached should not be true {daily_quote.error_message}"
    assert daily_quote.success, f"success is false {daily_quote.error_message}"
    assert len(daily_quote.data), f"Did not return data for this symbol {daily_quote.symbol}"
    logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


@pytest.mark.integration_paid
def test_can_quote_crypto():
    event = {
        "symbol": "ETH"
    }
    results = client.get_crypto_intraday(event)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    assert len(results.data), "Data{} property is empty but should have information"
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
    results = client.get_crypto_intraday(event)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    assert len(results.csv), "Data{} property is empty but should have information"
    logging.warning(f" Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")


@pytest.mark.integration
def test_can_quote_real_gdp():
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
    technical_indicator = client.get_technical_indicator(event)
    assert not technical_indicator.limit_reached, f"limit_reached is True {technical_indicator.error_message}"
    assert technical_indicator.success, f"Success is False {technical_indicator.error_message}"
    assert len(technical_indicator.csv), "Csv field is empty"
    logging.warning(" Can quote IBM EMA technical indicator")


@pytest.mark.integration
def test_can_query_company_overview():
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
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_company_overview(event)


@pytest.mark.integration
def test_can_not_query_income_statement():
    event = {
        "symbol": "tsla2"
    }

    accounting_report = client.get_income_statement(event)
    assert not accounting_report.success, f"success was found to be True: {accounting_report.error_message}"
    assert not accounting_report.limit_reached, f'{accounting_report.error_message}'
    assert accounting_report.symbol == event.get("symbol", None), f"Symbols don't match " \
                                                                  f"{accounting_report.symbol} : {event.get('symbol')}"
    logging.warning(f" Can not query  income statement {accounting_report.error_message}")


@pytest.mark.integration
def test_can_query_income_statement():
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
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_income_statement(event)


@pytest.mark.integration
def can_query_earnings():
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
        event = {
            "symbol": "tsla",
            "datatype": "csv"
        }
        client.get_earnings(event)


@pytest.mark.integration
def test_can_query_cash_flow():
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
    results = client.get_data_from_alpha_vantage(event)
    assert type(results) is dict, "Results object should be a dictionary"
    assert len(results) > 0, "There should be data in the results"

    logging.warning("Successfully queried data using get_data_from_alpha_vantage")

@pytest.mark.integration_paid
def test_get_fx_currency_data():
    event = {
        "function" : "CURRENCY_EXCHANGE_RATE",
        "from_currency" : "JPY",
        "to_currency" : "USD"
    }
    results = client.get_data_from_alpha_vantage(event)
    print(results)
    assert results["success"], f"FX Exchange call failed{results}"

@pytest.mark.integration
def test_get_market_status():
    market_status = client.get_market_status()
    print(market_status)
    assert market_status.success, f"success was found to be True which is unexpected: {market_status.error_message}"
    assert not market_status.limit_reached, f"limit_reached is true {market_status.error_message}"
    assert len(market_status.endpoint), "endPoint is not defined within response"
    assert len(market_status.data), "data list is missing results"

    for market in market_status.data:
        assert "market_type" in market, "market_type not found within result"
        assert "region" in market, "region not found within result"
        assert "primary_exchanges" in market, "primary_exchanges not found within result"
        assert "local_open" in market, "local_open not found within result"

@pytest.mark.integration
def test_get_news_and_sentiment():
    event = {
        "topics" : "earnings,technology",
        "limit" : "25"
    }
    news_and_sentiment = client.get_news_and_sentiment(event)
    assert news_and_sentiment.success, f"success was found to be True which is unexpected: {news_and_sentiment.error_message}"
    assert not news_and_sentiment.limit_reached, f"limit_reached is true {news_and_sentiment.error_message}"
    assert len(news_and_sentiment.sentiment_score_definition), "sentiment_score_definition is not defined within response"
    assert len(news_and_sentiment.data), "data list is missing results"

    for item in news_and_sentiment.data:
        assert "title" in item, "market_type not found within result"
        assert "url" in item, "region not found within result"
        assert "summary" in item, "primary_exchanges not found within result"
        assert "source" in item, "local_open not found within result"

@pytest.mark.integration
def test_get_market_movers():
    market_movers = client.get_top_gainers_and_losers()
    print(market_movers)
    assert market_movers.success, f"success was found to be True which is unexpected: {market_movers.error_message}"
    assert not market_movers.limit_reached, f"limit_reached is true {market_movers.error_message}"
    assert len(market_movers.meta_data), "meta_data is not defined within response"
    assert len(market_movers.top_gainers), "top_gainers list is missing results"
    assert len(market_movers.top_losers), "top_losers list is missing results"

    for item in market_movers.top_gainers:
        assert "ticker" in item, "ticker not found within result"
        assert "price" in item, "price not found within result"
        assert "change_amount" in item, "change_amount not found within result"
        assert "change_percentage" in item, "change_percentage not found within result"
        assert "volume" in item, "volume not found within result"

@pytest.mark.integration
def test_get_earnings_calendar():
    symbols = ["IBM", "AAPL", "AMZN", "MSFT", "TSLA", "SYM"]

    for symbol in symbols:
        event = {
            "symbol": symbol
        }
        earnings_calendar = client.get_earnings_calendar(event)
        assert earnings_calendar.success, f"success was found to be True which is unexpected: {earnings_calendar.error_message}"
        assert not earnings_calendar.limit_reached, f"limit_reached is true {earnings_calendar.error_message}"
        assert len(earnings_calendar.csv), "csv is not defined within response"
        assert len(earnings_calendar.data), "data is not defined within response"

        for item in earnings_calendar.data:
            print(item.json())

@pytest.mark.integration
def test_get_earnings_calendar():
    symbols = ["IBM", "AAPL", "AMZN", "MSFT", "TSLA", "SYM"]

    for symbol in symbols:
        event = {
            "symbol": symbol
        }
        earnings_calendar = client.get_earnings_calendar(event)
        assert earnings_calendar.success, f"success was found to be True which is unexpected: {earnings_calendar.error_message}"
        assert not earnings_calendar.limit_reached, f"limit_reached is true {earnings_calendar.error_message}"
        assert len(earnings_calendar.csv), "csv is not defined within response"
        assert len(earnings_calendar.data), "data is not defined within response"

        for item in earnings_calendar.data:
            print(item.json())

@pytest.mark.integration
def test_get_ipo_calendar():

    ipo_calendar = client.get_ipo_calendar()
    assert ipo_calendar.success, f"success was found to be True which is unexpected: {ipo_calendar.error_message}"
    assert not ipo_calendar.limit_reached, f"limit_reached is true {ipo_calendar.error_message}"
    assert len(ipo_calendar.csv), "csv is not defined within response"
    assert len(ipo_calendar.data), "data is not defined within response"

    for item in ipo_calendar.data:
        assert len(item.symbol), "csv is not defined within response"
        assert len(item.ipo_date), "ipo_date is not defined within response"
        assert len(item.name), "name is not defined within response"


@pytest.mark.integration
def test_get_forex_exchange_rates():
    event = {
        "from_currency": "USD",
        "to_currency" : "GBP"
    }
    quote = client.get_forex_exchange_rates(event)
    print(quote.json())

@pytest.mark.integration_paid
def test_get_forex_intraday_rates():
    event = {
        "from_symbol": "EUR",
        "to_symbol" : "USD"
    }
    currency_quote = client.get_forex_intraday(event)
    assert currency_quote.success, f"success was found to be True which is unexpected: {currency_quote.error_message}"
    assert not currency_quote.limit_reached, f"limit_reached is true {currency_quote.error_message}"
    assert len(currency_quote.meta_data), "meta_data is not defined within response"
    assert len(currency_quote.data), "data is not defined or zero within response"

@pytest.mark.integration
def test_get_forex_daily_rates():
    event = {
        "from_symbol": "EUR",
        "to_symbol" : "USD"
    }
    currency_quote = client.get_forex_daily(event)
    assert currency_quote.success, f"success was found to be True which is unexpected: {currency_quote.error_message}"
    assert not currency_quote.limit_reached, f"limit_reached is true {currency_quote.error_message}"
    assert len(currency_quote.meta_data), "meta_data is not defined within response"
    assert len(currency_quote.data), "data is not defined or zero within response"

@pytest.mark.integration
def test_get_forex_weekly_rates():
    event = {
        "from_symbol": "EUR",
        "to_symbol" : "USD"
    }
    currency_quote = client.get_forex_weekly(event)
    assert currency_quote.success, f"success was found to be True which is unexpected: {currency_quote.error_message}"
    assert not currency_quote.limit_reached, f"limit_reached is true {currency_quote.error_message}"
    assert len(currency_quote.meta_data), "meta_data is not defined within response"
    assert len(currency_quote.data), "data is not defined or zero within response"

@pytest.mark.integration
def test_get_forex_monthly_rates():
    event = {
        "from_symbol": "EUR",
        "to_symbol" : "USD"
    }
    currency_quote = client.get_forex_monthly(event)
    assert currency_quote.success, f"success was found to be True which is unexpected: {currency_quote.error_message}"
    assert not currency_quote.limit_reached, f"limit_reached is true {currency_quote.error_message}"
    assert len(currency_quote.meta_data), "meta_data is not defined within response"
    assert len(currency_quote.data), "data is not defined or zero within response"



