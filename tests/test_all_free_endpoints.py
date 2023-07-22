import pytest
from .test_base import BaseTestSuite
import time
from alphavantage_api_client import AlphavantageClient, CsvNotSupported, Ticker
import logging


class AllEndPointTests(BaseTestSuite):
    @pytest.mark.integration
    def test_can_get_global_quote_str(self):
        symbol = "tsla"
        global_quote = self.get_client().get_global_quote(symbol)
        assert (
            global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert (
            global_quote.symbol == symbol
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.data) > 0, "Response should have data but contains zero"
        logging.warning(f" Can quote stock symbol in JSON {symbol}")

    @pytest.mark.integration
    def test_can_get_global_quote_dict(self):
        event = {"symbol": "tsla"}

        global_quote = self.get_client().get_global_quote(event)
        assert (
            global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get(
            "symbol"
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.data) > 0, "Response should have data but contains zero"
        logging.warning(f" Can quote stock symbol in JSON {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_not_get_global_quote_dict(self):
        event = {"symbol": "tsla2"}

        global_quote = self.get_client().get_global_quote(event)
        assert (
            not global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get(
            "symbol"
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(
            f" Can Not quote stock symbol in JSON {event.get('symbol', None)}"
        )

    @pytest.mark.integration
    def test_can_not_get_global_quote_str(self):
        symbol = "tsla2"

        global_quote = self.get_client().get_global_quote(symbol)
        assert (
            not global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert (
            global_quote.symbol == symbol
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(f" Can Not quote stock symbol in JSON {symbol}")

    @pytest.mark.integration
    def test_can_get_global_quote_csv(self):
        event = {"symbol": "tsla", "datatype": "csv"}
        global_quote = self.get_client().get_global_quote(event)
        assert (
            global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get(
            "symbol"
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert len(global_quote.csv) > 0, "Response should have data but contains zero"
        logging.warning(f" Can quote stock symbol in CSV {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_not_global_quote_wrong_symbol_dict(self):
        event = {"symbol": "tsla2323"}
        global_quote = self.get_client().get_global_quote(event)
        assert (
            not global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get(
            "symbol"
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(
            f" Can NOT quote stock symbol in JSON {event.get('symbol', None)}"
        )

    @pytest.mark.integration
    def test_can_not_global_quote_wrong_symbol_str(self):
        symbol = "tsla2323"
        global_quote = self.get_client().get_global_quote(symbol)
        assert (
            not global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert (
            global_quote.symbol == symbol
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert not len(global_quote.data), "Response should have data but contains zero"
        logging.warning(f" Can NOT quote stock symbol in JSON {symbol}")

    @pytest.mark.integration
    def test_can_not_global_quote_wrong_symbol_csv(self):
        event = {"symbol": "tsla2233", "datatype": "csv"}
        global_quote = self.get_client().get_global_quote(event)
        assert (
            not global_quote.success
        ), f"success was found to be {global_quote.success}: {global_quote.error_message}"
        assert global_quote.symbol == event.get(
            "symbol"
        ), "Response symbol doesn't matched requested symbol"
        assert not global_quote.limit_reached, f"{global_quote.error_message}"
        assert global_quote.csv is None, "Response should have data but contains zero"
        logging.warning(
            f" Can NOT quote stock symbol in csv {event.get('symbol', None)} : {global_quote.error_message}"
        )

    @pytest.mark.integration
    def test_can_quote_intraday_dict(self):
        event = {
            "symbol": "TSLA",
            "datatype": "json",
            "function": "TIME_SERIES_INTRADAY",
            "interval": "5min",
        }
        quote = self.get_client().get_intraday_quote(event)
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(
            f" Successfully quoted intraday[dict] symbol {event['symbol']} in JSON"
        )

    @pytest.mark.integration
    def test_can_quote_intraday_str(self):
        symbol = "TSLA"
        quote = self.get_client().get_intraday_quote(symbol)
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted intraday[str] symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_can_quote_daily_adjusted_dict(self):
        event = {"symbol": "VZ"}
        quote = self.get_client().get_daily_adjusted_quote(event)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration  # here
    def test_can_quote_daily_adjusted_str(self):
        symbol = "VZ"
        quote = self.get_client().get_daily_adjusted_quote(symbol)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly_dict(self):
        event = {"symbol": "VZ"}
        quote = self.get_client().get_weekly_quote(event)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly_str(self):
        symbol = "VZ"
        quote = self.get_client().get_weekly_quote(symbol)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly_adjusted_dict(self):
        event = {"symbol": "VZ"}
        quote = self.get_client().get_weekly_adjusted_quote(event)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_weekly_adjusted_str(self):
        symbol = "VZ"
        quote = self.get_client().get_weekly_adjusted_quote(symbol)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_can_quote_monthly_dict(self):
        event = {"symbol": "VZ"}
        quote = self.get_client().get_monthly_quote(event)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")


    @pytest.mark.integration
    def test_can_quote_monthly_str(self):
        symbol = "VZ"
        quote = self.get_client().get_monthly_quote(symbol)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_can_quote_monthly_adjusted_dict(self):
        event = {"symbol": "VZ"}
        quote = self.get_client().get_monthly_adjusted_quote(event)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {event['symbol']} in JSON")

    @pytest.mark.integration
    def test_can_quote_monthly_adjusted_str(self):
        symbol = "VZ"
        quote = self.get_client().get_monthly_adjusted_quote(symbol)
        # print(quote.json())
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), f"Did not return data for this symbol {quote.symbol}"
        logging.warning(f" Successfully quoted symbol {symbol} in JSON")

    @pytest.mark.integration
    def test_get_intraday_with_params(self):
        symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
        for symbol in symbols:
            event = {"symbol": symbol, "adjusted": False, "interval": "60min"}
            intraday_quote = self.get_client().get_intraday_quote(event)
            assert (
                event["interval"] == intraday_quote.meta_data["4. Interval"]
            ), f"The interval doesn't match, {event['interval']} != {intraday_quote.meta_data['4. Interval']}"

    @pytest.mark.integration
    def test_get_daily_quote_with_params(self):
        symbols = ["TSLA", "MSFT", "AMZN", "TDOC", "PATH", "ZM", "C", "VZ"]
        for symbol in symbols:
            event = {"adjusted": False, "outputsize": "compact", "symbol": symbol}
            daily_quote = self.get_client().get_daily_quote(event)
            expected_output_size = event["outputsize"].upper()
            given_output_size = None
            if "4. Output Size" in daily_quote.meta_data:
                given_output_size = daily_quote.meta_data["4. Output Size"].upper()
            assert (
                expected_output_size == given_output_size
            ), f"The interval doesn't match, {expected_output_size} != {given_output_size}"

    @pytest.mark.integration
    def test_can_search_ticker(self):
        event = {"keywords": "Tesla"}
        ticker_search_result = self.get_client().search_ticker(event)
        assert (
            not ticker_search_result.limit_reached
        ), f"limit_reached should not be true {ticker_search_result.error_message}"
        assert (
            ticker_search_result.success
        ), f"success is false {ticker_search_result.error_message}"
        assert len(
            ticker_search_result.data
        ), f"Did not return bestMatches for this search {event['keywords']}"
        for result in ticker_search_result.data:
            assert (
                "9. matchScore" in result
            ), f"9. matchScore property is not in search result for {event['keywords']}"
            assert (
                "1. symbol" in result
            ), f"1. symbol property is not in search result for {event['keywords']}"
            assert (
                "2. name" in result
            ), f"2. name property is not in search result for {event['keywords']}"
            assert (
                "3. type" in result
            ), f"3. type property is not in search result for {event['keywords']}"

    @pytest.mark.integration
    def test_get_news_and_sentiment(self):
        event = {"topics": "earnings,technology", "limit": "25"}
        news_and_sentiment = self.get_client().get_news_and_sentiment(event)
        assert (
            news_and_sentiment.success
        ), f"success was found to be True which is unexpected: {news_and_sentiment.error_message}"
        assert (
            not news_and_sentiment.limit_reached
        ), f"limit_reached is true {news_and_sentiment.error_message}"
        assert len(
            news_and_sentiment.sentiment_score_definition
        ), "sentiment_score_definition is not defined within response"
        assert len(news_and_sentiment.data), "data list is missing results"

        for item in news_and_sentiment.data:
            assert "title" in item, "market_type not found within result"
            assert "url" in item, "region not found within result"
            assert "summary" in item, "primary_exchanges not found within result"
            assert "source" in item, "local_open not found within result"

    @pytest.mark.integration
    def test_get_market_movers(self):
        market_movers = self.get_client().get_top_gainers_and_losers()
        # print(market_movers)
        assert (
            market_movers.success
        ), f"success was found to be True which is unexpected: {market_movers.error_message}"
        assert (
            not market_movers.limit_reached
        ), f"limit_reached is true {market_movers.error_message}"
        assert len(market_movers.meta_data), "meta_data is not defined within response"
        assert len(market_movers.top_gainers), "top_gainers list is missing results"
        assert len(market_movers.top_losers), "top_losers list is missing results"

        for item in market_movers.top_gainers:
            assert "ticker" in item, "ticker not found within result"
            assert "price" in item, "price not found within result"
            assert "change_amount" in item, "change_amount not found within result"
            assert (
                "change_percentage" in item
            ), "change_percentage not found within result"
            assert "volume" in item, "volume not found within result"

    @pytest.mark.integration
    def test_can_query_company_overview_dict(self):
        event = {"symbol": "TSLA"}

        company_overview = self.get_client().get_company_overview(event)
        assert (
            company_overview.success
        ), f"Unable to get comapny overview {company_overview.error_message}"
        assert company_overview.symbol == event.get(
            "symbol"
        ), f"Symbols are not equal {company_overview.symbol} : {event.get('symbol')}"
        assert not company_overview.limit_reached, "unexpected limit_reached"
        logging.warning(f" Can query company overview {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_query_company_overview_str(self):
        symbol = "TSLA"

        company_overview = self.get_client().get_company_overview(symbol)
        assert (
            company_overview.success
        ), f"Unable to get comapny overview {company_overview.error_message}"
        assert company_overview.symbol == symbol, f"Symbols are not equal {company_overview.symbol} : {symbol}"
        assert not company_overview.limit_reached, "unexpected limit_reached"
        logging.warning(f" Can query company overview {symbol}")

    @pytest.mark.integration
    def test_can_not_quote_company_overview(self):
        event = {"symbol": "TSLA2"}

        company_overview = self.get_client().get_company_overview(event)
        assert (
            not company_overview.success
        ), f"{event.get('symbol')} should not have been successful"
        assert company_overview.symbol != event.get(
            "symbol"
        ), f"Symbols are equal {company_overview.symbol} : {event.get('symbol')} but shouldn't be"
        assert not company_overview.limit_reached, "unexpected limit_reached"
        logging.warning(
            f" Can not query company overview: {company_overview.error_message}"
        )

    @pytest.mark.integration
    def test_can_not_query_csv_company_overview(self):
        with pytest.raises(CsvNotSupported):
            event = {"symbol": "tsla", "datatype": "csv"}
            self.get_client().get_company_overview(event)

    @pytest.mark.integration
    def test_can_not_query_income_statement(self):
        event = {"symbol": "tsla22354q2354"}
        accounting_report = self.get_client().get_income_statement(event)
        assert (
            not accounting_report.success
        ), f"success was found to be True: {accounting_report.error_message}"
        assert accounting_report.symbol == event.get("symbol", None), (
            f"Symbols don't match "
            f"{accounting_report.symbol} : {event.get('symbol')}"
        )
        logging.warning(
            f" Can not query  income statement {accounting_report.error_message}"
        )

    @pytest.mark.integration
    def test_can_query_income_statement_dict(self):
        event = {"symbol": "tsla"}

        accounting_report = self.get_client().get_income_statement(event)
        assert (
            accounting_report.success
        ), f"success was found to be false: {accounting_report.error_message}"
        assert not accounting_report.limit_reached, f"{accounting_report.error_message}"
        assert accounting_report.symbol == event.get("symbol", None), (
            f"Symbols don't match "
            f"{accounting_report.symbol} : {event.get('symbol')}"
        )
        logging.warning(f" Can query  income statement {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_query_income_statement_str(self):
        symbol = "TSLA"

        accounting_report = self.get_client().get_income_statement(symbol)
        assert (
            accounting_report.success
        ), f"success was found to be false: {accounting_report.error_message}"
        assert not accounting_report.limit_reached, f"{accounting_report.error_message}"
        assert accounting_report.symbol == symbol, (
            f"Symbols don't match "
            f"{accounting_report.symbol} : {symbol}"
        )
        logging.warning(f" Can query  income statement {symbol}")

    @pytest.mark.integration
    def test_can_not_query_income_statement_csv(self):
        with pytest.raises(CsvNotSupported):
            event = {"symbol": "tsla", "datatype": "csv"}
            self.get_client().get_income_statement(event)

    @pytest.mark.integration
    def test_fiscal_date_ending_field_in_all_accounting_reports(self):
        ticker = Ticker().use_client(self.get_client())
        vz = ticker.from_symbol("VZ").fetch_accounting_reports()
        earnings = vz.get_earnings()
        income_statement = vz.get_income_statement()
        balance_sheet = vz.get_balance_sheet()
        cash_flow = vz.get_cash_flow()

        for index, account_report in enumerate(earnings.annualReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(earnings.quarterlyReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(income_statement.quarterlyReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(income_statement.quarterlyReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(balance_sheet.quarterlyReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(balance_sheet.annualReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(cash_flow.quarterlyReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        for index, account_report in enumerate(cash_flow.annualReports):
            assert (
                "fiscalDateEnding" in account_report
            ), f"Did not find fiscalDateEnding in {account_report}"

        logging.warning("Found fiscalDateEnding in all accounting reports")

    # todo - missing tests for balance sheet

    @pytest.mark.integration
    def test_can_query_cash_flow_dict(self):
        event = {"symbol": "tsla"}

        cash_flow = self.get_client().get_cash_flow(event)
        assert (
            cash_flow.success
        ), f"success was found to be false: {cash_flow.error_message}"
        assert (
            not cash_flow.limit_reached
        ), f"limit_reached is true {cash_flow.error_message}"
        assert cash_flow.symbol == event.get(
            "symbol"
        ), f"Symbols do not match {cash_flow.symbol} : {event.get('symbol')}"
        assert len(cash_flow.annualReports), "annualReports is empty"
        assert len(cash_flow.quarterlyReports), "quarterlyReports are empty"
        logging.warning(f" Can query  cash flow {event.get('symbol', None)}")

    @pytest.mark.integration
    def test_can_query_cash_flow_str(self):
        symbol = "TSLA"

        cash_flow = self.get_client().get_cash_flow(symbol)
        assert (
            cash_flow.success
        ), f"success was found to be false: {cash_flow.error_message}"
        assert (
            not cash_flow.limit_reached
        ), f"limit_reached is true {cash_flow.error_message}"
        assert cash_flow.symbol == symbol, f"Symbols do not match {cash_flow.symbol} : {symbol}"
        assert len(cash_flow.annualReports), "annualReports is empty"
        assert len(cash_flow.quarterlyReports), "quarterlyReports are empty"
        logging.warning(f" Can query  cash flow {symbol}")

    @pytest.mark.integration
    def test_can_not_query_cash_flow(self):
        event = {"symbol": "tsla22"}

        cash_flow = self.get_client().get_cash_flow(event)
        assert (
            not cash_flow.success
        ), f"success was found to be True which is unexpected: {cash_flow.error_message}"
        assert (
            not cash_flow.limit_reached
        ), f"limit_reached is true {cash_flow.error_message}"
        assert cash_flow.symbol == event.get(
            "symbol"
        ), f"Symbols do not match {cash_flow.symbol} : {event.get('symbol')}"
        assert not len(cash_flow.annualReports), "annualReports are not empty"
        assert not len(cash_flow.quarterlyReports), "quarterlyReports are not empty"
        logging.warning(f" Can not query  cash flow {cash_flow.error_message}")
        

    @pytest.mark.integration
    def test_can_not_query_cash_flow_csv(self):
        with pytest.raises(CsvNotSupported):
            event = {"symbol": "tsla", "datatype": "csv"}
            self.get_client().get_cash_flow(event)
            logging.warning(
                f"Querying  cash flow as CSV threw error as expected {event.get('symbol', None)}"
            )

    @pytest.mark.integration
    def can_query_earnings_dict(self):
        event = {"symbol": "tsla"}

        earnings = self.get_client().get_earnings(event)
        assert (
            earnings.success
        ), f"success was found to be false: {earnings.error_message}"
        assert not earnings.limit_reached, f"{earnings.error_message}"
        assert len(earnings.quarterlyReports), "quarterlyReports is empty"
        assert len(earnings.annualReports), "annualReports is empty"
        assert earnings.symbol == event.get(
            "symbol"
        ), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
        logging.warning(f" Can query  earnings {event.get('symbol', None)}")

    @pytest.mark.integration
    def can_query_earnings_str(self):
        symbol = "TSLA"

        earnings = self.get_client().get_earnings(symbol)
        assert (
            earnings.success
        ), f"success was found to be false: {earnings.error_message}"
        assert not earnings.limit_reached, f"{earnings.error_message}"
        assert len(earnings.quarterlyReports), "quarterlyReports is empty"
        assert len(earnings.annualReports), "annualReports is empty"
        assert earnings.symbol == symbol, f"Symbols not equal {earnings.symbol} : {symbol}"
        logging.warning(f" Can query  earnings {symbol}")

    @pytest.mark.integration
    def test_can_not_query_earnings(self):
        event = {"symbol": "tsla22"}

        earnings = self.get_client().get_earnings(event)
        assert (
            not earnings.success
        ), f"success was found to be false: {earnings.error_message}"
        assert (
            not earnings.limit_reached
        ), f"limit_reached is not present in results {earnings.error_message}"
        assert earnings.symbol == event.get(
            "symbol"
        ), f"Symbols not equal {earnings.symbol} : {event.get('symbol')}"
        logging.warning(f" Can not query earnings: {earnings.error_message}")

    @pytest.mark.integration
    def test_can_not_query_earnings_csv(self):
        with pytest.raises(CsvNotSupported):
            event = {"symbol": "tsla", "datatype": "csv"}
            self.get_client().get_earnings(event)

    @pytest.mark.integration
    def test_get_ipo_calendar(self):
        ipo_calendar = self.get_client().get_ipo_calendar()
        assert (
            ipo_calendar.success
        ), f"success was found to be True which is unexpected: {ipo_calendar.error_message}"
        assert (
            not ipo_calendar.limit_reached
        ), f"limit_reached is true {ipo_calendar.error_message}"
        assert len(ipo_calendar.csv), "csv is not defined within response"
        assert len(ipo_calendar.data), "data is not defined within response"

        for item in ipo_calendar.data:
            assert len(item.symbol), "csv is not defined within response"
            assert len(item.ipo_date), "ipo_date is not defined within response"
            assert len(item.name), "name is not defined within response"

    @pytest.mark.integration
    def test_get_earnings_calendar(self):
        symbols = ["IBM", "AAPL", "AMZN", "MSFT", "TSLA", "SYM"]

        for symbol in symbols:
            event = {
                "symbol": symbol,
                "horizon": "6month" #6 months so we are sure to get data
                }
            earnings_calendar = self.get_client().get_earnings_calendar(event)
            assert (
                earnings_calendar.success
            ), f"success was found to be True which is unexpected: {earnings_calendar.error_message}"
            assert (
                not earnings_calendar.limit_reached
            ), f"limit_reached is true {earnings_calendar.error_message}"
            assert len(earnings_calendar.csv), "csv is not defined within response"
            assert len(earnings_calendar.data), "data is not defined within response"

            for item in earnings_calendar.data:
                # print(item.json())
                pass

    # todo - add tests for listing & delisting status

    @pytest.mark.integration
    def test_get_forex_daily_rates(self):
        event = {"from_symbol": "EUR", "to_symbol": "USD"}
        currency_quote = self.get_client().get_forex_daily(event)
        assert (
            currency_quote.success
        ), f"success was found to be True which is unexpected: {currency_quote.error_message}"
        assert (
            not currency_quote.limit_reached
        ), f"limit_reached is true {currency_quote.error_message}"
        assert len(currency_quote.meta_data), "meta_data is not defined within response"
        assert len(currency_quote.data), "data is not defined or zero within response"

    @pytest.mark.integration
    def test_get_forex_weekly_rates(self):
        event = {"from_symbol": "EUR", "to_symbol": "USD"}
        currency_quote = self.get_client().get_forex_weekly(event)
        assert (
            currency_quote.success
        ), f"success was found to be True which is unexpected: {currency_quote.error_message}"
        assert (
            not currency_quote.limit_reached
        ), f"limit_reached is true {currency_quote.error_message}"
        assert len(currency_quote.meta_data), "meta_data is not defined within response"
        assert len(currency_quote.data), "data is not defined or zero within response"

    @pytest.mark.integration
    def test_get_forex_monthly_rates(self):
        event = {"from_symbol": "EUR", "to_symbol": "USD"}
        currency_quote = self.get_client().get_forex_monthly(event)
        assert (
            currency_quote.success
        ), f"success was found to be True which is unexpected: {currency_quote.error_message}"
        assert (
            not currency_quote.limit_reached
        ), f"limit_reached is true {currency_quote.error_message}"
        assert len(currency_quote.meta_data), "meta_data is not defined within response"
        assert len(currency_quote.data), "data is not defined or zero within response"

    @pytest.mark.integration
    def test_can_quote_crypto_daily(self):
        event = {"symbol": "ETH"}
        quote = self.get_client().get_crypto_daily(event)
        # print(quote)
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), "Data{} property is empty but should have information"
        logging.warning(
            f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON"
        )

    @pytest.mark.integration
    def test_can_quote_crypto_weekly(self):
        event = {"symbol": "ETH"}
        quote = self.get_client().get_crypto_weekly(event)
        # print(quote)
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), "Data{} property is empty but should have information"
        logging.warning(
            f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON"
        )

    @pytest.mark.integration
    def test_can_quote_crypto_monthly(self):
        event = {"symbol": "ETH"}
        quote = self.get_client().get_crypto_monthly(event)
        # print(quote)
        assert (
            not quote.limit_reached
        ), f"limit_reached should not be true {quote.error_message}"
        assert quote.success, f"success is false {quote.error_message}"
        assert len(quote.data), "Data{} property is empty but should have information"
        logging.warning(
            f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON"
        )
        logging.warning(
            f" Successfully quoted cryptocurrency symbol {event['symbol']} in JSON"
        )

    @pytest.mark.integration
    def test_can_quote_currency_exchange_rates(self):
        event = {"from_currency": "BTC", "to_currency": "CNY"}
        currency_quote = self.get_client().get_currency_exchange_rates(event)
        assert (
            not currency_quote.limit_reached
        ), f"limit_reached should not be true {currency_quote.error_message}"
        assert (
            currency_quote.success
        ), f"success is false {currency_quote.error_message}"
        assert len(
            currency_quote.data
        ), "Data{} property is empty but should have information"
        logging.warning(
            f" Successfully quoted cryptocurrency symbol {event['from_currency']} to {event['to_currency']} in JSON"
        )

    @pytest.mark.integration
    def test_get_crude_oil_wti(self):
        client = AlphavantageClient()
        event = {"interval": "daily"}
        crude_wti = self.get_client().get_crude_oil_wti_prices(event)
        name = crude_wti.name
        assert (
            crude_wti.success
        ), f"success was found to be False: {crude_wti.error_message}"
        assert (
            not crude_wti.limit_reached
        ), f"limit_reached is true {crude_wti.error_message}"
        assert len(crude_wti.data), f"data is empty, we should have {name} prices"
        assert name == "Crude Oil Prices WTI", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_crude_oil_brent(self):
        event = {"interval": "daily"}
        crude_brent = self.get_client().get_crude_oil_brent_prices(event)
        name = crude_brent.name
        assert (
            crude_brent.success
        ), f"success was found to be False: {crude_brent.error_message}"
        assert (
            not crude_brent.limit_reached
        ), f"limit_reached is true {crude_brent.error_message}"
        assert len(crude_brent.data), f"data is empty, we should have {name} prices"
        assert name == "Crude Oil Prices Brent", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_natural_gas(self):
        event = {"interval": "daily"}
        natural_gas = self.get_client().get_natural_gas_prices(event)
        name = natural_gas.name
        assert (
            natural_gas.success
        ), f"success was found to be False: {natural_gas.error_message}"
        assert (
            not natural_gas.limit_reached
        ), f"limit_reached is true {natural_gas.error_message}"
        assert len(natural_gas.data), f"data is empty, we should have {name} prices"
        assert name == "Henry Hub Natural Gas Spot Price", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_copper(self):
        event = {"interval": "daily"}
        copper = self.get_client().get_copper_prices(event)
        name = copper.name
        assert copper.success, f"success was found to be False: {copper.error_message}"
        assert not copper.limit_reached, f"limit_reached is true {copper.error_message}"
        assert len(copper.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Copper", f"You are not testing {name}"

    def test_get_aluminum(self):
        event = {"interval": "daily"}
        aluminum = self.get_client().get_aluminum_prices(event)
        name = aluminum.name
        assert (
            aluminum.success
        ), f"success was found to be False: {aluminum.error_message}"
        assert (
            not aluminum.limit_reached
        ), f"limit_reached is true {aluminum.error_message}"
        assert len(aluminum.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Aluminum", f"You are not testing {name}"

    def test_get_wheat(self):
        event = {"interval": "daily"}
        wheat = self.get_client().get_wheat_prices(event)
        name = wheat.name
        assert wheat.success, f"success was found to be False: {wheat.error_message}"
        assert not wheat.limit_reached, f"limit_reached is true {wheat.error_message}"
        assert len(wheat.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Wheat", f"You are not testing {name}"

    def test_get_corn(self):
        event = {"interval": "daily"}
        corn = self.get_client().get_corn_prices(event)
        name = corn.name
        assert corn.success, f"success was found to be False: {corn.error_message}"
        assert not corn.limit_reached, f"limit_reached is true {corn.error_message}"
        assert len(corn.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Corn", f"You are not testing {name}"

    def test_get_cotton(self):
        event = {"interval": "daily"}
        cotton = self.get_client().get_cotton_prices(event)
        name = cotton.name
        assert cotton.success, f"success was found to be False: {cotton.error_message}"
        assert not cotton.limit_reached, f"limit_reached is true {cotton.error_message}"
        assert len(cotton.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Cotton", f"You are not testing {name}"

    def test_get_sugar(self):
        event = {"interval": "daily"}
        sugar = self.get_client().get_sugar_prices(event)
        name = sugar.name
        assert sugar.success, f"success was found to be False: {sugar.error_message}"
        assert not sugar.limit_reached, f"limit_reached is true {sugar.error_message}"
        assert len(sugar.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Sugar", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_coffee_commodity(self):
        event = {"interval": "daily"}
        coffee = self.get_client().get_coffee_prices(event)
        name = coffee.name
        assert coffee.success, f"success was found to be False: {coffee.error_message}"
        assert not coffee.limit_reached, f"limit_reached is true {coffee.error_message}"
        assert len(coffee.data), f"data is empty, we should have {name} prices"
        assert name == "Global Price of Coffee", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_all_commodities(self):
        event = {"interval": "daily"}
        all_commodities = self.get_client().get_all_commodity_prices(event)
        name = all_commodities.name
        assert (
            all_commodities.success
        ), f"success was found to be False: {all_commodities.error_message}"
        assert (
            not all_commodities.limit_reached
        ), f"limit_reached is true {all_commodities.error_message}"
        assert len(all_commodities.data), f"data is empty, we should have {name} prices"
        assert (
            name == "Global Price Index of All Commodities"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_can_quote_real_gdp(self):
        real_gdp = self.get_client().get_real_gdp()
        assert (
            not real_gdp.limit_reached
        ), f"limit_reached is not present in results {real_gdp.error_message}"
        assert (
            real_gdp.success
        ), f"Success=False but expected true  {real_gdp.error_message}"
        assert len(real_gdp.data), "Data{} is empty but expected results"
        logging.warning(" Can quote Real GDP")

    @pytest.mark.integration
    def test_can_quote_real_gdp_csv(self):
        event = {"interval": "annual", "datatype": "csv"}
        real_gdp = self.get_client().get_real_gdp(event)
        assert (
            not real_gdp.limit_reached
        ), f"limit_reached is not present in results {real_gdp.error_message}"
        assert (
            real_gdp.success
        ), f"Success=False but expected true  {real_gdp.error_message}"
        assert real_gdp.data is None, "Data{} is empty but expected results"
        assert len(real_gdp.csv), "CSV data is not present"
        logging.warning(" Can quote Real GDP")

    @pytest.mark.integration
    def test_get_real_gdp_per_capita(self):
        real_gdp_per_capita = self.get_client().get_real_gdp_per_capita()
        name = real_gdp_per_capita.name
        assert (
            real_gdp_per_capita.success
        ), f"success was found to be False: {real_gdp_per_capita.error_message}"
        assert (
            not real_gdp_per_capita.limit_reached
        ), f"limit_reached is true {real_gdp_per_capita.error_message}"
        assert len(
            real_gdp_per_capita.data
        ), f"data is empty, we should have {name} prices"
        assert (
            name == "Real Gross Domestic Product per Capita"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_treasury_yield(self):
        treasury_yield = self.get_client().get_treasury_yield()
        name = treasury_yield.name
        assert (
            treasury_yield.success
        ), f"success was found to be False: {treasury_yield.error_message}"
        assert (
            not treasury_yield.limit_reached
        ), f"limit_reached is true {treasury_yield.error_message}"
        assert len(treasury_yield.data), f"data is empty, we should have {name}"
        assert name.endswith(
            "Treasury Constant Maturity Rate"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_federal_funds_rate(self):
        treasury_yield = self.get_client().get_federal_funds_rate()
        name = treasury_yield.name
        assert (
            treasury_yield.success
        ), f"success was found to be False: {treasury_yield.error_message}"
        assert (
            not treasury_yield.limit_reached
        ), f"limit_reached is true {treasury_yield.error_message}"
        assert len(treasury_yield.data), f"data is empty, we should have {name}"
        assert name == "Effective Federal Funds Rate", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_cpi(self):
        cpi = self.get_client().get_cpi()
        name = cpi.name
        assert cpi.success, f"success was found to be False: {cpi.error_message}"
        assert not cpi.limit_reached, f"limit_reached is true {cpi.error_message}"
        assert len(cpi.data), f"data is empty, we should have {name}"
        assert (
            name == "Consumer Price Index for all Urban Consumers"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_inflation(self):
        inflation = self.get_client().get_cpi()
        name = inflation.name
        assert (
            inflation.success
        ), f"success was found to be False: {inflation.error_message}"
        assert (
            not inflation.limit_reached
        ), f"limit_reached is true {inflation.error_message}"
        assert len(inflation.data), f"data is empty, we should have {name}"
        assert (
            name == "Consumer Price Index for all Urban Consumers"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_retail_sales(self):
        retail_sales = self.get_client().get_retails_sales()
        name = retail_sales.name
        assert (
            retail_sales.success
        ), f"success was found to be False: {retail_sales.error_message}"
        assert (
            not retail_sales.limit_reached
        ), f"limit_reached is true {retail_sales.error_message}"
        assert len(retail_sales.data), f"data is empty, we should have {name}"
        assert (
            name == "Advance Retail Sales: Retail Trade"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_durable_goods_orders(self):
        durable_goods_orders = self.get_client().get_durable_goods_orders()
        name = durable_goods_orders.name
        assert (
            durable_goods_orders.success
        ), f"success was found to be False: {durable_goods_orders.error_message}"
        assert (
            not durable_goods_orders.limit_reached
        ), f"limit_reached is true {durable_goods_orders.error_message}"
        assert len(durable_goods_orders.data), f"data is empty, we should have {name}"
        assert (
            name == "Manufacturer New Orders: Durable Goods"
        ), f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_unemployment(self):
        unemployment = self.get_client().get_unemployment()
        name = unemployment.name
        assert (
            unemployment.success
        ), f"success was found to be False: {unemployment.error_message}"
        assert (
            not unemployment.limit_reached
        ), f"limit_reached is true {unemployment.error_message}"
        assert len(unemployment.data), f"data is empty, we should have {name}"
        assert name == "Unemployment Rate", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_nonfarm_payroll(self):
        nonfarm_payroll = self.get_client().get_nonfarm_payroll()
        name = nonfarm_payroll.name
        assert (
            nonfarm_payroll.success
        ), f"success was found to be False: {nonfarm_payroll.error_message}"
        assert (
            not nonfarm_payroll.limit_reached
        ), f"limit_reached is true {nonfarm_payroll.error_message}"
        assert len(nonfarm_payroll.data), f"data is empty, we should have {name}"
        assert name == "Total Nonfarm Payroll", f"You are not testing {name}"

    @pytest.mark.integration
    def test_get_market_status(self):
        market_status = self.get_client().get_market_status()
        # print(market_status)
        assert (
            market_status.success
        ), f"success was found to be True which is unexpected: {market_status.error_message}"
        assert (
            not market_status.limit_reached
        ), f"limit_reached is true {market_status.error_message}"
        assert len(market_status.endpoint), "endPoint is not defined within response"
        assert len(market_status.data), "data list is missing results"

        for market in market_status.data:
            assert "market_type" in market, "market_type not found within result"
            assert "region" in market, "region not found within result"
            assert (
                "primary_exchanges" in market
            ), "primary_exchanges not found within result"
            assert "local_open" in market, "local_open not found within result"

    @pytest.mark.technical_indicator
    def test_get_sma_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_sma(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Simple Moving Average (SMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_sma_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_sma(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Simple Moving Average (SMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ema_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ema(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Exponential Moving Average (EMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ema_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_ema(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Exponential Moving Average (EMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_wma_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_wma(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Weighted Moving Average (WMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_wma_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_wma(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Weighted Moving Average (WMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_dema_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_dema(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Double Exponential Moving Average (DEMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_dema_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_dema(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Double Exponential Moving Average (DEMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_tema_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_tema(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triple Exponential Moving Average (TEMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_tema_str(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_tema(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triple Exponential Moving Average (TEMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_trima_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_trima(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triangular Exponential Moving Average (TRIMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_trima_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_trima(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triangular Exponential Moving Average (TRIMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_kama_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_kama(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Kaufman Adaptive Moving Average (KAMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_kama_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_kama(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Kaufman Adaptive Moving Average (KAMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_mama_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_mama(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "MESA Adaptive Moving Average (MAMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_mama_str(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_mama(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "MESA Adaptive Moving Average (MAMA)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_vwap_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_vwap(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Volume Weighted Average Price (VWAP)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_vwap_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_vwap(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Volume Weighted Average Price (VWAP)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_t3_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_t3(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triple Exponential Moving Average (T3)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_t3_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_t3(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Triple Exponential Moving Average (T3)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_macd_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_macd(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Moving Average Convergence/Divergence (MACD)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_macd_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_macd(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Moving Average Convergence/Divergence (MACD)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_macdext_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_macdext(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "MACD with Controllable MA Type (MACDEXT)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_macdext_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_macdext(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "MACD with Controllable MA Type (MACDEXT)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stoch_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_stoch(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Stochastic (STOCH)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stoch_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_stoch(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Stochastic (STOCH)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stochf_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_stockhf(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Stochastic Fast (STOCHF)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stochf_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_stockhf(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Stochastic Fast (STOCHF)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_rsi_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_rsi(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Relative Strength Index (RSI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_rsi_str(self):
        symbol = "TSLA"
        sma = self.get_client().get_rsi(symbol)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Relative Strength Index (RSI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stochrsi_dict(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_stochrsi(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Stochastic Relative Strength Index (STOCHRSI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_stochrsi_str(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_stochrsi(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Stochastic Relative Strength Index (STOCHRSI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_willr(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_willr(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Williams' %R (WILLR)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_adx(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_adx(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Average Directional Movement Index (ADX)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_adxr(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_adxr(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Average Directional Movement Index Rating (ADXR)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_apo(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_apo(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Absolute Price Oscillator (APO)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ppo(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ppo(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Percentage Price Oscillator (PPO)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_mom(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_mom(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Momentum (MOM)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_bop(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_bop(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Balance Of Power (BOP)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_cci(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_bop(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Balance Of Power (BOP)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_cmo(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_cmo(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Chande Momentum Oscillator (CMO)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_roc(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_roc(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Rate of change : ((price/prevPrice)-1)*100"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_rocr(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_rocr(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Rate of change ratio: (price/prevPrice)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_aroon(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_aroon(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Aroon (AROON)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_aroonosc(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_aroonosc(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Aroon Oscillator (AROONOSC)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_mfi(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_mfi(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Money Flow Index (MFI)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_trix(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_trix(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "1-day Rate-Of-Change (ROC) of a Triple Smooth EMA (TRIX)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ultosc(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ultosc(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Ultimate Oscillator (ULTOSC)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_dx(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_dx(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Directional Movement Index (DX)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_minus_di(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_minus_di(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Minus Directional Indicator (MINUS_DI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_plus_di(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_plus_di(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Plus Directional Indicator (PLUS_DI)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_minus_dm(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_minus_dm(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Minus Directional Movement (MINUS_DM)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_plus_dm(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_plus_dm(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Plus Directional Movement (PLUS_DM)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_bbands(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_bbands(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Bollinger Bands (BBANDS)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_midpoint(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_midpoint(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "MidPoint over period (MIDPOINT)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_midprice(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_midprice(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Midpoint Price over period (MIDPRICE)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_sar(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_sar(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Parabolic SAR (SAR)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_trange(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_trange(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "True Range (TRANGE)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_atr(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_atr(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Average True Range (ATR)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_natr(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_natr(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Normalized Average True Range (NATR)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ad(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ad(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "Chaikin A/D Line", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_adosc(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_adosc(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Chaikin A/D Oscillator (ADOSC)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_obv(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_obv(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert name == "On Balance Volume (OBV)", f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_trendline(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_trendline(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - Instantaneous Trendline (HT_TRENDLINE)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_sine(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_sine(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - SineWave (HT_SINE)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_trendmode(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_trendmode(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - Trend vs Cycle Mode (HT_TRENDMODE)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_dcperiod(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_dcperiod(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - Dominant Cycle Period (HT_DCPERIOD)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_dcphase(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_dcphase(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - Dominant Cycle Phase (HT_DCPHASE)"
        ), f"You are testing the wrong end point"

    @pytest.mark.technical_indicator
    def test_get_ht_phasor(self):
        event = {"symbol": "TSLA"}
        sma = self.get_client().get_ht_phasor(event)
        assert len(sma.meta_data), f"meta_data is empty"
        assert len(
            sma.meta_data["2: Indicator"]
        ), f"2: Indicator is missing from technical indicator"
        name = sma.meta_data["2: Indicator"]
        assert sma.success, f"success was found to be False: {sma.error_message}"
        assert not sma.limit_reached, f"limit_reached is true {sma.error_message}"
        assert len(sma.data), f"data is empty, we should have data for {name}"
        assert (
            name == "Hilbert Transform - Phasor Components (HT_PHASOR)"
        ), f"You are testing the wrong end point"
