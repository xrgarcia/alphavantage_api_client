from alphavantage_api_client import Ticker
import pytest


@pytest.mark.integration
def test_retry_obtain_global_quote():
    print("")
    symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
    ticker = Ticker().create_client().should_retry_once()
    for symbol in symbols:
        ticker.from_symbol(symbol).fetch_global_quote().fetch_company_overview()
        global_quote = ticker.get_global_quote()
        company_overview = ticker.get_company_overview()
        print(symbol, global_quote.get_open_price(), company_overview.get_ex_dividend_date())

    metrics = ticker.get_client().get_internal_metrics()
    print("")
    print(metrics)


@pytest.mark.integration
def test_get_most_recent_intraday():
    print("")
    symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
    ticker = Ticker().create_client().should_retry_once()
    for symbol in symbols:
        latest_quote = ticker.from_symbol(symbol).fetch_intraday_quote().get_intraday_quote().get_most_recent_value()
        print(symbol, latest_quote)

    metrics = ticker.get_client().get_internal_metrics()
    print("")
    print(metrics)


@pytest.mark.integration
def test_get_most_recent_annual_reports():
    print("")
    symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
    ticker = Ticker().create_client().should_retry_once()
    for symbol in symbols:
        ticker.from_symbol(symbol).fetch_earnings()
        latest_annual_report = ticker.get_earnings().get_most_recent_annual_report()
        latest_quarterly_report = ticker.get_earnings().get_most_recent_quarterly_report()
        print(symbol, latest_annual_report, latest_quarterly_report)

    metrics = ticker.get_client().get_internal_metrics()
    print("")
    print(metrics)


@pytest.mark.integration
def test_get_intraday_with_params():
    print("")
    params = {
        "adjusted": False,
        "interval": "60min"
    }
    symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
    ticker = Ticker().create_client().should_retry_once()
    for symbol in symbols:
        intraday_quote = ticker.from_symbol(symbol).fetch_intraday_quote(params).get_intraday_quote()
        assert params["interval"] == intraday_quote.meta_data["4. Interval"], \
            f"The interval doesn't match, {params['interval']} != {intraday_quote.meta_data['4. Interval']}"

@pytest.mark.integration
def test_get_daily_quote_with_params():
    print("")
    params = {
        "adjusted": False,
        "interval": "60min"
    }
    symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
    ticker = Ticker().create_client().should_retry_once()
    for symbol in symbols:
        daily_quote = ticker.from_symbol(symbol).fetch_daily_quote(params).get_daily_quote()
        assert params["interval"] == daily_quote.meta_data["4. Interval"], \
            f"The interval doesn't match, {params['interval']} != {daily_quote.meta_data['4. Interval']}"

