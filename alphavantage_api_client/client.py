import time

import requests
import os
import configparser
from .response_validation_rules import ValidationRuleChecks
import json
from alphavantage_api_client.models import (
    GlobalQuote,
    Quote,
    AccountingReport,
    CompanyOverview,
    EconomicIndicator,
    CsvNotSupported,
    TickerSearch,
    MarketStatus,
    NewsAndSentiment,
    MarketMovers,
    EarningsCalendar,
    IpoCalendarItem,
    IpoCalendar,
    CurrencyQuote,
    Commodity,
)
import copy
import logging
import hashlib
from typing import Optional, Union
import csv


class ApiKeyNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AlphavantageClient:
    """Python wrapper around alpha vantage api

    Create a simple python wrapper around alpha vantage api. Normalize responses so you have consistency across end points.
    Provide direct access to each end point so customers who already use the API can have the flexibility. Make it easy
    to debug, so users can track down issues quickly.

        Typical usage example:

            client = AlphavantageClient()
            or
            client = AlphavantageClient().should_retry_once().use_simple_cache()
    """

    def __init__(self):
        self.__total_calls__ = 0
        self.__max_cache_size__ = 0
        self.__retry__ = False
        self.__first_successful_attempt__ = 0
        self.__use_cache__ = False
        self.__cache__ = {}
        # try to get api key from USER_PROFILE/.alphavantage
        alphavantage_config_file_path = (
            f'{os.path.expanduser("~")}{os.path.sep}.alphavantage'
        )
        msg = {
            "method": "__init__",
            "action": f"{alphavantage_config_file_path} config file found",
        }
        if os.path.exists(alphavantage_config_file_path):
            logging.info(json.dumps(msg))
            config = configparser.ConfigParser()
            config.read(alphavantage_config_file_path)
            self.__api_key__ = config["access"]["api_key"]
            return
        # try to get from an environment variable
        elif os.environ.get("ALPHAVANTAGE_API_KEY") is not None:
            self.__api_key__ = os.environ.get("ALPHAVANTAGE_API_KEY")
            msg["action"] = f"api key found from environment"
            logging.info(json.dumps(msg))
            return
        else:
            self.__api_key__ = ""

    def __build_url_from_args__(self, event: dict):
        """private method to construct a url from requested api configuration

        Args:
            event: the params

        Returns:
            a string in url format
        """
        url = f"https://www.alphavantage.co/query?"
        # build url from event
        for property in event:
            url += f"{property}={event[property]}&"
        url = url[:-1]
        return url

    def __inject_values__(self, default_values: dict, dest_obj: dict):
        """private method: inserts values into the destination dict. This will not overwrite values

        Args:
            default_values: The required values to be inserted into the dest_obj
            dest_obj: the dict to be hydrated with the default_values

        Returns:
            None

        """
        # inject defaults for missing values
        for default_key in default_values:
            if default_key not in dest_obj or dest_obj[default_key] is None:
                dest_obj[default_key] = default_values[default_key]

    def __create_api_request_from__(self, defaults: dict, event: Union[str, dict]):
        json_request = event
        if isinstance(event, str):
            json_request = {"symbol": event} #assume the symbol
        elif json_request is not None:
            json_request = event.copy()
        else:
            json_request = {}
        self.__inject_values__(defaults, json_request)

        return json_request

    def should_retry_once(self, retry: bool = True):
        """Retry api call when limit reached has been detected

        At present the Alpha Vantage API only allows 5 calls per min with a free account. This means you would need to
        build retry logic to maximize your calls.  We have already done that for you! As a result, the client
        will calculate the time from the last call and pause up to a minute before making a subsequent call.

        Args:
            retry: Flag to indicate whether you want to retry when limit has been reached

        Returns:
            AlphavantageClient

        """
        self.__retry__ = retry

        return self

    def use_simple_cache(self, use_cache: bool = True, max_cache_size: int = 100):
        """First in / First Out Cache to reduce the amount of calls you need to make to the alpha vantage api

        An In-Memory Caching mechanism where your parameters (i.e. symbol, function, interval, format, etc) are used as
        a key into a dictionary. This is similar to how SQL uses the SQL statement to cache it's responses. If you
        have already requested data with those attributes then it will simply return it from the cache. The cache will
        continue to grow until you call the clear_cache()


        First in First Out Cache
        Args:
            use_cache: Flag to indicate whether you want to turn on caching
            max_cache_size: Max size of the cache.

        Returns:

        """
        self.__use_cache__ = use_cache
        self.__max_cache_size__ = max_cache_size

        return self

    def get_internal_metrics(self) -> dict:
        """Obtain the total calls, retry setting and the first successful attempt

        We want to provide you will some usefull statistics that may help you troubleshoot or understand your usage.

        Returns:
            A dict of relevaant details about your usage
            totals calls - how many total calls have been made by the client
            retry - your retry flag
            first_successful_attempt - the time as a float

        """
        total_calls = self.__total_calls__
        retry = self.__retry__
        first_successful_attempt = self.__first_successful_attempt__
        metrics = {
            "total_calls": total_calls,
            "retry": retry,
            "first_successful_attempt": first_successful_attempt,
        }
        return metrics

    def with_api_key(self, api_key: str):
        """Specify your alpha vantage API Key

        There are a few ways you can specify your alpha vantage api key:
        1. This method ;-)
        2. ~/.alphavantage
        3. ALPHAVANTAGE_API_KEY env variable
        4. within each request event dict using the same key name as the api expects (i.e. apiKey)

        Args:
            api_key (str): Your api key from alpha vantage

        Returns:
            This AlphavantageClient
        """
        if api_key is None or len(api_key) == 0:
            raise ApiKeyNotFound(
                "API Key is null or empty. Please specify a valid api key"
            )
        self.__api_key__ = api_key

        return self

    def get_global_quote(self, event: Union[str, dict]) -> GlobalQuote:
        """A lightweight alternative to the time series APIs

        This service returns the price and volume information
        for the equity of your choice.
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            A GlobalQuote for the requested equity

        """

        defaults = {"function": "GLOBAL_QUOTE"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return GlobalQuote.model_validate(json_response)

    def get_daily_quote(self, event: Union[str, dict]) -> Quote:
        """As traded daily time series price history

        Includes: date, daily open, daily high, daily low, daily close, daily
        volume for your specified equity covering 20+ years of historical data. If you are also interested in
        split/dividend-adjusted historical data, please use the get_daily_adjusted_quote(...), which covers adjusted
        close values and historical split and dividend events.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {
            "datatype": "json",
            "function": "TIME_SERIES_DAILY",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_daily_adjusted_quote(self, event: Union[str, dict]) -> Quote:
        """As-traded daily open/high/low/close/volume values

        Daily adjusted close values, and historical split/dividend events of the global equity specified, covering
        20+ years of historical data.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {
            "datatype": "json",
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_weekly_quote(self, event: Union[str, dict]) -> Quote:
        """weekly time series trading data

        This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low,
        weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {
            "datatype": "json",
            "function": "TIME_SERIES_WEEKLY",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_weekly_adjusted_quote(self, event: Union[str, dict]) -> Quote:
        """weekly adjusted time series trading data

        This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high,
        weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the global equity
        specified, covering 20+ years of historical data.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_WEEKLY_ADJUSTED"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_monthly_quote(self, event: Union[str, dict]) -> Quote:
        """monthly time series trading data

        This API returns monthly time series (last trading day of each month, monthly open, monthly high,
        monthly low, monthly close, monthly volume) of the global equity specified, covering 20+ years
        of historical data.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_MONTHLY"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_monthly_adjusted_quote(self, event: Union[str, dict]) -> Quote:
        """monthly adjusted time series trading data

        This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high,
        monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified,
        covering 20+ years of historical data.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote for the requested equity

        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_MONTHLY_ADJUSTED"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_intraday_quote(self, event: Union[str, dict]) -> Quote:
        """Intraday time series data covering extended trading hours.

        Covering extended trading hours when applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market).
        The intraday data is derived from the Securities Information Processor (SIP) market-aggregated data.
        You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint.
        This API returns the most recent 1-2 months of intraday data and is best suited for short-term/medium-term
        charting and trading strategy development.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
             The Quote for the requested equity

        """
        # default params
        defaults = {
            "symbol": None,
            "datatype": "json",
            "function": "TIME_SERIES_INTRADAY",
            "interval": "60min",
            "outputsize": "compact"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_income_statement(self, event: Union[str, dict]) -> AccountingReport:
        """annual and quarterly income statements for the company of interest

        Includes normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally
        refreshed on the same day a company reports its latest earnings and financials.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The AccountingReport for the requested equity

        """

        defaults = {"function": "INCOME_STATEMENT", "datatype": "json"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {"symbol": event}
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.model_validate(json_response)

    def get_balance_sheet(self, event: Union[str, dict]) -> AccountingReport:
        """annual and quarterly balance sheets for the company of interest

        Includes normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the
        same day a company reports its latest earnings and financials.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The AccountingReport for the requested equity

        """
        defaults = {"function": "BALANCE_SHEET", "datatype": "json"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {"symbol": event}
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)

        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.model_validate(json_response)

    def get_cash_flow(self, event: Union[str, dict]) -> AccountingReport:
        """annual and quarterly cash flow for the company of interest

        Includes normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on
        the same day a company reports its latest earnings and financials.
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The AccountingReport for the requested equity

        """
        defaults = {"function": "CASH_FLOW", "datatype": "json"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {"symbol": event}
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.model_validate(json_response)

    def get_earnings(self, event: Union[str, Union[str, dict]]) -> AccountingReport:
        """annual and quarterly earnings (EPS) for the company of interest

        The quarterly data also includes analyst estimates and surprise metrics.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The AccountingReport for the requested equity

        """
        defaults = {"function": "EARNINGS", "datatype": "json"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {"symbol": event}

        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.model_validate(json_response)

    def get_company_overview(self, event: Union[str, dict]) -> CompanyOverview:
        """company information, financial ratios, and other key metrics for the equity specified.

        Data is generally refreshed on the same day a company reports its latest earnings and financials.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The CompanyOverview for the requested equity

        """
        defaults = {"function": "OVERVIEW"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {"symbol": event}
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CompanyOverview.model_validate(json_response)

    def get_crypto_intraday(self, event: dict) -> CurrencyQuote:
        """Returns crypto intraday time series price data

        Includes: timestamp, open, high, low, close, volume of the cryptocurrency specified, updated realtime.

        Args:
            event: dict of parameters to be sent to the API

        Returns:
            The CurrencyQuote for the requested equity

        """
        defaults = {
            "function": "CRYPTO_INTRADAY",
            "market": "USD",
            "interval": "60min",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        # print(json.dumps(json_response))
        return CurrencyQuote.model_validate(json_response)

    def get_crypto_daily(self, event: dict) -> CurrencyQuote:
        """returns the daily historical time series for a digital currency (e.g., BTC)

        refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific 
        currency and USD traded on a specific market (e.g., CNY/Chinese Yuan)

        Args:
            event: A dict of parameters that will be passed to the api.

        Returns:
            The CurrencyQuote for the requested equity

        """
        defaults = {"function": "DIGITAL_CURRENCY_DAILY", "market": "CNY"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        return CurrencyQuote.model_validate(json_response)

    def get_crypto_weekly(self, event: dict) -> CurrencyQuote:
        """Returns the daily historical time series for a digital currency (e.g., BTC)

        As traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC). Prices and
        volumes are quoted in both the market-specific currency and USD.

        Args:
            event: A dict of parameters that will be passed to the api.

        Returns:
            The CurrencyQuote for the requested equity

        """
        defaults = {"function": "DIGITAL_CURRENCY_WEEKLY", "market": "CNY"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        return CurrencyQuote.model_validate(json_response)

    def get_crypto_monthly(self, event: dict) -> CurrencyQuote:
        """Returns the monthly historical time series for a digital currency (e.g., BTC)

        Refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

        Args:
            event: A dict of parameters that will be passed to the api.

        Returns:
            The CurrencyQuote for the requested equity

        """
        defaults = {"function": "DIGITAL_CURRENCY_MONTHLY", "market": "CNY"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        return CurrencyQuote.model_validate(json_response)

    def get_currency_exchange_rates(self, event: dict) -> CurrencyQuote:
        """returns the exchange rate for any pair of digital currency (e.g., Bitcoin) or physical currency (e.g., USD).

        Args:
            event: A Dictionary of parameters that will be passed to the api.

        Returns:
            The CurrencyQuote for the requested equity

        """
        defaults = {"function": "CURRENCY_EXCHANGE_RATE"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        return CurrencyQuote.model_validate(json_response)

    def get_real_gdp(self, event: dict = None) -> EconomicIndicator:
        """Returns the annual and quarterly Real GDP of the United States.

        Source: U.S. Bureau of Economic Analysis, Real Gross Domestic Product, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {"function": "REAL_GDP", "interval": "annual", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_treasury_yield(self, event: dict = None) -> EconomicIndicator:
        """Returns the daily, weekly, and monthly US treasury yield of a given maturity timeline.

        Source: Board of Governors of the Federal Reserve System (US), Market Yield on U.S. Treasury Securities
        at 3-month, 2-year, 5-year, 7-year, 10-year, and 30-year Constant Maturities, Quoted on an Investment Basis,
        retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed
        or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the
        FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "TREASURY_YIELD",
            "interval": "monthly",
            "datatype": "json",
            "maturity": "10year",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_federal_funds_rate(self, event: dict = None) -> EconomicIndicator:
        """returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.

        Source: Board of Governors of the Federal Reserve System (US), Federal Funds Effective Rate, retrieved from
        FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/FEDFUNDS). This data feed uses the
        FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed,
        you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "FEDERAL_FUNDS_RATE",
            "interval": "monthly",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_cpi(self, event: dict = None) -> EconomicIndicator:
        """Returns the monthly and semiannual consumer price index (CPI) of the United States.

        CPI is widely regarded as the barometer of inflation levels in the broader economy.
        Source: U.S. Bureau of Labor Statistics, Consumer Price Index for All Urban Consumers: All Items in U.S. City
        Average, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not
        endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be
        bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {"function": "CPI", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_inflation(self, event: dict = None) -> EconomicIndicator:
        """Returns the annual inflation rates (consumer prices) of the United States.

        Source: World Bank, Inflation, consumer prices for the United States, retrieved from FRED, Federal Reserve Bank
        of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve
        Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "INFLATION",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_retails_sales(self, event: dict = None) -> EconomicIndicator:
        """returns the monthly Advance Retail Sales: Retail Trade data of the United States.

        Source: U.S. Census Bureau, Advance Retail Sales: Retail Trade, retrieved from FRED,
        Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/RSXFSN). This data feed uses the FRED®
        API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you
        agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "RETAIL_SALES",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_durable_goods_orders(self, event: dict = None) -> EconomicIndicator:
        """Returns the monthly manufacturers' new orders of durable goods in the United States.

        Source: U.S. Census Bureau, Manufacturers' New Orders: Durable Goods, retrieved from FRED, Federal Reserve
        Bank of St. Louis (https://fred.stlouisfed.org/series/UMDMNO). This data feed uses the FRED® API but is not
        endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound
        by the FRED® API Terms of Use.

        Args:
            event (dict): Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "DURABLES",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_unemployment(self, event: dict = None) -> EconomicIndicator:
        """Returns the monthly unemployment data of the United States.

        The unemployment rate represents the number of unemployed as a percentage of the labor force. Labor force
        data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the
        District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged),
        and who are not on active duty in the Armed Forces (source).

        Source: U.S. Bureau of Labor Statistics, Unemployment Rate, retrieved from FRED, Federal Reserve Bank of
        St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of
        St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "UNEMPLOYMENT",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_nonfarm_payroll(self, event: dict = None) -> EconomicIndicator:
        """Returns the monthly US All Employees Nonfarm, a measure of the number of U.S.

        Workers in the economy that excludes proprietors, private household employees, unpaid volunteers,
        farm employees, and the unincorporated self-employed.

        Source: U.S. Bureau of Labor Statistics, All Employees, Total Nonfarm, retrieved from FRED, Federal Reserve
        Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve
        Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            The EconomicIndicator for the requested equity

        """
        defaults = {
            "function": "NONFARM_PAYROLL",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_real_gdp_per_capita(self, event: dict = None) -> EconomicIndicator:
        """Returns the quarterly Real GDP per Capita data of the United States.

        Source: U.S. Bureau of Economic Analysis, Real gross domestic product per capita, retrieved from FRED,
        Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the
        Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: Not required. You can pass in any parameters supported by the api

        Returns:
            :rtype: EconomicIndicator

        """
        defaults = {"function": "REAL_GDP_PER_CAPITA", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return EconomicIndicator.model_validate(json_response)

    def get_technical_indicator(self, event: dict) -> Quote:
        """
        Default technical indicator is SMA. You can change this by passing in ``function`` = ``[your indicator]``

        Args:
            event (dict): Parameters supported by the API

        Returns:
            :rtype: Quote

        """
        defaults = {"function": "SMA", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        json_response["indicator"] = event.get("function")

        return Quote.model_validate(json_response)

    def get_data_from_alpha_vantage(
        self, event: dict, should_retry: bool = False
    ) -> dict:
        """Underlying function that talks to alphavantage api.

        Feel free to pass in any parameters supported by the api.  You will receive a dictionary with the response
        from the web api. In addition, you will obtain the success, error_message and limit_reached fields.
        Args:
            event: dict of the url parameters supported by the web api

        Returns:
            A dict of the response from alpha vantage api. success, error_message and limit_reached fields are injected
            into the dict for your reference.

        """
        # validate api key and insert into the request if needed
        checks = ValidationRuleChecks().from_customer_request(event)
        self.__validate_api_key__(checks, event)

        # create a version of the event without api key
        loggable_event = copy.deepcopy(event)
        loggable_event.pop("apikey")

        # check cache if allowed
        if self.__use_cache__:
            results = self.__get_item_from_cache__(loggable_event)
            logging.info(f"Found item in cache: {results}")
            if results is not None:
                return results

        # fetch data from API
        self.__fetch_data__(checks, event, loggable_event)
        requested_data = {}

        # hydrate the response
        self.__hydrate_request__(requested_data, checks, event, should_retry)

        # retry once if allowed and needed
        if checks.expect_limit_not_reached().passed() and should_retry:
            self.__sleep__()
            result = self.get_data_from_alpha_vantage(event, False)
            self.__first_successful_attempt__ = time.perf_counter()
            return result

        # not all calls will have a symbol in the call to alphavantage.... if so we can, capture it.
        if "symbol" in event:
            requested_data["symbol"] = event["symbol"]

        # put into cache if allowed
        if self.__use_cache__:
            self.__put_item_into_cache__(loggable_event, requested_data)

        logging.info(
            json.dumps(
                {
                    "method": "get_data_from_alpha_vantage",
                    "action": "return_value",
                    "data": requested_data,
                    "event": loggable_event,
                }
            )
        )

        return requested_data

    def __put_item_into_cache__(self, event, results):
        if len(self.__cache__) >= self.__max_cache_size__:
            self.__cache__.clear()

        hash_str = json.dumps(event, sort_keys=True)
        self.__cache__[hash_str] = results

    def __get_item_from_cache__(self, event):
        hash_str = json.dumps(event, sort_keys=True)
        if hash_str in self.__cache__:
            return self.__cache__[hash_str]

        return None

    def __hydrate_request__(
        self,
        requested_data: dict,
        checks: ValidationRuleChecks,
        event: dict,
        should_retry: bool,
    ):
        # verify request worked correctly and build response
        # gotta check if consumer request json or csv, so we can parse the output correctly
        requested_data[
            "success"
        ] = checks.expect_successful_response().passed()  # successful csv response
        if not requested_data["success"]:
            requested_data["Error Message"] = checks.get_error_message()
        requested_data["limit_reached"] = checks.expect_limit_not_reached().passed()
        requested_data["status_code"] = checks.get_status_code()

        if (
            checks.expect_json_datatype().expect_successful_response().passed()
        ):  # successful json response
            json_response = checks.get_obj()
            for field in json_response:
                requested_data[field] = json_response[field]

        if (
            checks.expect_csv_datatype().expect_successful_response().passed()
        ):  # successful csv response
            requested_data["csv"] = checks.get_obj()

    def __fetch_data__(
        self, checks: ValidationRuleChecks, event: dict, loggable_event: dict
    ):
        url = self.__build_url_from_args__(event)
        r = requests.get(url)
        if self.__first_successful_attempt__ == 0:
            self.__first_successful_attempt__ = time.perf_counter()
        self.__total_calls__ += 1
        checks.with_response(r)
        logging.info(
            json.dumps(
                {
                    "method": "get_data_from_alpha_vantage",
                    "action": "response_from_alphavantage",
                    "status_code": r.status_code,
                    "data": r.text,
                    "event": loggable_event,
                }
            )
        )

    def __validate_api_key__(self, checks: ValidationRuleChecks, event: dict):
        # get api key if not provided
        if checks.expect_api_key_in_event().failed():
            event["apikey"] = self.__api_key__  # assume they passed to builder method.
        elif (
            self.__api_key__ is None
            or len(self.__api_key__) == 0
            or "apikey" not in event
            or not event.get("apikey")
        ):  # consumer didn't tell me where to get api key
            raise ApiKeyNotFound(
                "You must call client.with_api_key([api_key]), create config file in your profile (i.e. ~/.alphavantage) or event[api_key] = [your api key] before retrieving data from alphavantage"
            )

    def __sleep__(self):
        then = self.__first_successful_attempt__
        now = time.perf_counter()
        diff = 60 - (now - then)
        logging.info(f"sleeping for {diff} seconds")
        if diff < 0:
            diff = 60
        time.sleep(diff)

    def clear_cache(self):
        """Clear First in / First Out Cache

        Returns:
            Nothing

        """
        self.__cache__.clear()

        return self

    def search_ticker(self, event: dict) -> TickerSearch:
        """The Search Endpoint returns the best-matching symbols and market information based on your keywords.

        The search results also contain match scores that provide you with the full
        flexibility to develop your own search and filtering logic.
        Args:
            event: dict

        Returns:
            TickerSearch

        """
        defaults = {"function": "SYMBOL_SEARCH", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return TickerSearch.model_validate(json_response)

    def get_market_status(self) -> MarketStatus:
        """Returns the current market status of major trading venues for equities, forex, and cryptocurrencies.

        Returns:
            The MarketStatus of your choice
        """
        json_request = {"function": "MARKET_STATUS"}
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return MarketStatus.model_validate(json_response)

    def get_top_gainers_and_losers(self) -> MarketMovers:
        """Returns the top 20 gainers, losers, and the most active traded tickers in the US market.

        Returns:
            The MarketMovers of your choice

        """
        json_request = {"function": "TOP_GAINERS_LOSERS"}
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return MarketMovers.model_validate(json_response)

    def get_earnings_calendar(self, event: Union[str, dict]) -> EarningsCalendar:
        """Returns a list of company earnings expected in the next 3, 6, or 12 months.

        Returns:
            The EarningsCalendar of your choice

        """
        defaults = {
            "function": "EARNINGS_CALENDAR",
            "horizon": "3month",
            "datatype": "csv",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        records = json_response["csv"].split("\n")
        header = records.pop(0)
        headers = header.split(",")
        reader = csv.DictReader(records, delimiter=",")
        reader.fieldnames = headers
        items = list(reader)
        json_response["data"] = items

        return EarningsCalendar.model_validate(json_response)

    def get_ipo_calendar(self) -> IpoCalendar:
        """Returns a list of company earnings expected in the next 3, 6, or 12 months.

        Returns:
            The IpoCalendar of your choice

        """
        json_request = {"function": "IPO_CALENDAR", "datatype": "csv"}

        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        records = json_response["csv"].split("\n")
        header = records.pop(0)
        headers = header.split(",")
        reader = csv.DictReader(records, delimiter=",")
        reader.fieldnames = headers
        items = list(reader)
        json_response["data"] = items

        return IpoCalendar.model_validate(json_response)

    def get_news_and_sentiment(self, event: dict) -> NewsAndSentiment:
        """Returns live and historical market news & sentiment data

        This API returns live and historical market news & sentiment data derived from over 50 major financial news
        outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal
        policy, mergers & acquisitions, IPOs, etc.

        Args:
            event: dict

        Returns:
            The NewsAndSentiment of your choice

        """
        defaults = {"function": "NEWS_SENTIMENT", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return NewsAndSentiment.model_validate(json_response)

    def get_forex_intraday(self, event: dict) -> CurrencyQuote:
        """returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified.

        Args:
            event: dict containing your params to the api

        Returns:
            The CurrencyQuote of your choice

        """
        defaults = {
            "function": "FX_INTRADAY",
            "datatype": "json",
            "interval": "60min",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CurrencyQuote.model_validate(json_response)

    def get_forex_daily(self, event: dict) -> CurrencyQuote:
        """returns the daily time series of the FX currency pair specified, updated realtime.

        Included fields: (timestamp, open, high, low, close)

        Args:
            event: dict containing your params to the api

        Returns:
            The CurrencyQuote of your choice

        """

        defaults = {
            "function": "FX_DAILY",
            "datatype": "json",
            "interval": "60min",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CurrencyQuote.model_validate(json_response)

    def get_forex_weekly(self, event: dict) -> CurrencyQuote:
        """returns the weekly time series of the FX currency pair specified

        Included fields: (timestamp, open, high, low, close) updated in realtime.  The latest data point is the price
        information for the week (or partial week) containing the current trading day, updated realtime.

        Args:
            event: dict containing your params to the api

        Returns:
            The CurrencyQuote of your choice
        """
        defaults = {
            "function": "FX_WEEKLY",
            "datatype": "json",
            "interval": "60min",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CurrencyQuote.model_validate(json_response)

    def get_forex_monthly(self, event: dict) -> CurrencyQuote:
        """returns the monthly time series of the FX currency pair specified

        Included fields: (timestamp, open, high, low, close) updated in realtime.  The latest data point is the prices
        information for the month (or partial month containing the current trading day, updated realtime.

        Args:
            event: dict containing your params to the api

        Returns:
            The CurrencyQuote of your choice

        """
        defaults = {
            "function": "FX_MONTHLY",
            "datatype": "json",
            "interval": "60min",
            "outputsize": "compact",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CurrencyQuote.model_validate(json_response)

    def get_crude_oil_wti_prices(self, event: dict) -> Commodity:
        """returns the West Texas Intermediate (WTI) crude oil prices in daily, weekly, and monthly horizons.

        Source: U.S. Energy Information Administration, Crude Oil Prices: West Texas Intermediate (WTI) - Cushing,
        Oklahoma, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not
        endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be
        bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "WTI", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_crude_oil_brent_prices(self, event: dict) -> Commodity:
        """returns the Brent (Europe) crude oil prices in daily, weekly, and monthly horizons.

        Source: U.S. Energy Information Administration, Crude Oil Prices: Brent - Europe, retrieved from FRED,
        Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the
        Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "BRENT", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_natural_gas_prices(self, event: dict) -> Commodity:
        """returns the Henry Hub natural gas spot prices in daily, weekly, and monthly horizons.

        Source: U.S. Energy Information Administration, Henry Hub Natural Gas Spot Price, retrieved from FRED,
        Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the
        Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {
            "function": "NATURAL_GAS",
            "interval": "monthly",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_copper_prices(self, event: dict) -> Commodity:
        """returns the global price of copper in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Copper, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice
        """
        defaults = {"function": "COPPER", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_aluminum_prices(self, event: dict) -> Commodity:
        """returns the global price of aluminum in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Aluminum, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "ALUMINUM", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_wheat_prices(self, event: dict) -> Commodity:
        """returns the global price of wheat in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Wheat, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "WHEAT", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_corn_prices(self, event: dict) -> Commodity:
        """returns the global price of corn in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Corn, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice
        """
        defaults = {"function": "CORN", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_cotton_prices(self, event: dict) -> Commodity:
        """returns the global price of cotton in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Cotton, retrieved from FRED, Federal
        Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal
        Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "COTTON", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_sugar_prices(self, event: dict) -> Commodity:
        """returns the global price of sugar in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Sugar, No. 11, World, retrieved from
        FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by
        the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound
        by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "SUGAR", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_coffee_prices(self, event: dict) -> Commodity:
        """returns the global price of coffee in monthly, quarterly, and annual horizons.

        Source: International Monetary Fund (IMF Terms of Use), Global price of Coffee, Other Mild Arabica,
        retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not
        endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be
        bound by the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {"function": "COFFEE", "interval": "monthly", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_all_commodity_prices(self, event: dict) -> Commodity:
        """returns the global price index of all commodities in monthly, quarterly, and annual temporal dimensions.

        Source: International Monetary Fund (IMF Terms of Use), Global Price Index of All Commodities, retrieved
        from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or
        certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by
        the FRED® API Terms of Use.

        Args:
            event: dict containing your params to the api

        Returns:
            The Commodity of your choice

        """
        defaults = {
            "function": "ALL_COMMODITIES",
            "interval": "monthly",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Commodity.model_validate(json_response)

    def get_sma(self, event: Union[str, dict]) -> Quote:
        """Returns the simple moving average (SMA) values.

        See also:   http://www.investopedia.com/articles/technical/052201.asp
                    http://www.fmlabs.com/reference/default.htm?url=SimpleMA.htm
        Args:
            event:  A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "SMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ema(self, event: Union[str, dict]) -> Quote:
        """returns the exponential moving average (EMA) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=ExpMA.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "EMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_wma(self, event: Union[str, dict]) -> Quote:
        """returns the exponential moving average (EMA) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=ExpMA.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "WMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_dema(self, event: Union[str, dict]) -> Quote:
        """returns the double exponential moving average (DEMA) values.

        See also: http://www.investopedia.com/articles/trading/10/double-exponential-moving-average.asp
                : http://www.fmlabs.com/reference/default.htm?url=DEMA.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "DEMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_tema(self, event: Union[str, dict]) -> Quote:
        """returns the triple exponential moving average (TEMA) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=TEMA.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "TEMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_trima(self, event: Union[str, dict]) -> Quote:
        """returns the triple exponential moving average (TEMA) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=TEMA.htm
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "TRIMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_kama(self, event: Union[str, dict]) -> Quote:
        """returns the Kaufman adaptive moving average (KAMA) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "KAMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_mama(self, event: Union[str, dict]) -> Quote:
        """returns the MESA adaptive moving average (MAMA) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "MAMA",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_vwap(self, event: Union[str, dict]) -> Quote:
        """returns the volume weighted average price (VWAP) for intraday time series.

        See also: https://www.investopedia.com/terms/v/vwap.asp

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {"function": "VWAP", "interval": "60min", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_t3(self, event: Union[str, dict]) -> Quote:
        """returns the triple exponential moving average (T3) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=T3.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "T3",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_macd(self, event: Union[str, dict]) -> Quote:
        """returns the moving average convergence / divergence (MACD) values.

        See also: http://www.investopedia.com/articles/forex/05/macddiverge.asp
                : http://www.fmlabs.com/reference/default.htm?url=MACD.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "MACD",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_macdext(self, event: Union[str, dict]) -> Quote:
        """returns the moving average convergence / divergence values with controllable moving average type.

        See also: http://www.investopedia.com/articles/forex/05/macddiverge.asp
                : http://www.fmlabs.com/reference/default.htm?url=MACD.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "MACDEXT",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_stoch(self, event: Union[str, dict]) -> Quote:
        """returns the stochastic oscillator (STOCH) values.

        See also: https://www.investopedia.com/terms/s/stochasticoscillator.asp
                : http://www.fmlabs.com/reference/default.htm?url=StochasticOscillator.htm
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns:
            The Quote of your choice

        """
        defaults = {
            "function": "STOCH",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_stockhf(self, event: Union[str, dict]) -> Quote:
        """returns the stochastic fast (STOCHF) values.

        See also: http://www.investopedia.com/university/indicator_oscillator/ind_osc8.asp
                : http://www.fmlabs.com/reference/default.htm?url=StochasticOscillator.htm
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "STOCHF", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_rsi(self, event: Union[str, dict]) -> Quote:
        """returns the relative strength index (RSI) values.

        See also: http://www.investopedia.com/articles/technical/071601.asp
                : http://www.fmlabs.com/reference/default.htm?url=RSI.htm
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "RSI",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_stochrsi(self, event: Union[str, dict]) -> Quote:
        """returns the stochastic relative strength index (STOCHRSI) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=StochRSI.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote
        """
        defaults = {
            "function": "STOCHRSI",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_willr(self, event: Union[str, dict]) -> Quote:
        """returns the Williams' %R (WILLR) values.

        See also: http://www.fmlabs.com/reference/default.htm?url=WilliamsR.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "WILLR",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_adx(self, event: Union[str, dict]) -> Quote:
        """ returns the average directional movement index (ADX) values.
        
        See also: http://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp
                : http://www.fmlabs.com/reference/default.htm?url=ADX.htm
        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "ADX",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_adxr(self, event: Union[str, dict]) -> Quote:
        """ returns the average directional movement index rating (ADXR) values.
        This API 
        See also: http://www.fmlabs.com/reference/default.htm?url=ADXR.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "ADXR",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_apo(self, event: Union[str, dict]) -> Quote:
        """ returns the absolute price oscillator (APO) values.
        
        See also: http://www.fmlabs.com/reference/default.htm?url=PriceOscillator.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "APO",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ppo(self, event: Union[str, dict]) -> Quote:
        """ returns the percentage price oscillator (PPO) values.
        
        See also: http://www.investopedia.com/articles/investing/051214/use-percentage-price-oscillator-elegant-indicator-picking-stocks.asp
                : http://www.fmlabs.com/reference/default.htm?url=PriceOscillatorPct.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "PPO",
            "interval": "daily",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_mom(self, event: Union[str, dict]) -> Quote:
        """returns the momentum (MOM) values.
        
        See also: http://www.investopedia.com/articles/technical/03/070203.asp
                : http://www.fmlabs.com/reference/default.htm?url=Momentum.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MOM",
            "interval": "daily",
            "series_type": "close",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_bop(self, event: Union[str, dict]) -> Quote:
        """returns the balance of power (BOP) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "BOP", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_cci(self, event: Union[str, dict]) -> Quote:
        """returns the commodity channel index (CCI) values.
        
        See also: http://www.investopedia.com/articles/trading/05/041805.asp
                : http://www.fmlabs.com/reference/default.htm?url=CCI.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "CCI",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_cmo(self, event: Union[str, dict]) -> Quote:
        """returns the Chande momentum oscillator (CMO) values.
        
        See also: http://www.fmlabs.com/reference/default.htm?url=CMO.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "CMO",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_roc(self, event: Union[str, dict]) -> Quote:
        """returns the rate of change (ROC) values.
        
        See also: http://www.investopedia.com/articles/technical/092401.asp

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "ROC",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_rocr(self, event: Union[str, dict]) -> Quote:
        """returns the rate of change ratio (ROCR) values.
        
        See also: http://www.investopedia.com/articles/technical/092401.asp

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "ROCR",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_aroon(self, event: Union[str, dict]) -> Quote:
        """returns the Aroon (AROON) values.
        
        See also: http://www.investopedia.com/articles/trading/06/aroon.asp
                : http://www.fmlabs.com/reference/default.htm?url=Aroon.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "AROON",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_aroonosc(self, event: Union[str, dict]) -> Quote:
        """returns the Aroon oscillator (AROONOSC) values.
        
        See also: http://www.fmlabs.com/reference/default.htm?url=AroonOscillator.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "AROONOSC",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_mfi(self, event: Union[str, dict]) -> Quote:
        """returns the money flow index (MFI) values.
        
        See also: http://www.investopedia.com/articles/technical/03/072303.asp
                : http://www.fmlabs.com/reference/default.htm?url=MoneyFlowIndex.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MFI",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_trix(self, event: Union[str, dict]) -> Quote:
        """returns the 1-day rate of change of a triple smooth exponential moving average (TRIX) values.
        
        See also: http://www.investopedia.com/articles/technical/02/092402.asp
                : http://www.fmlabs.com/reference/default.htm?url=TRIX.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "TRIX",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ultosc(self, event: Union[str, dict]) -> Quote:
        """returns the ultimate oscillator (ULTOSC) values.
        
        See also: http://www.fmlabs.com/reference/default.htm?url=UltimateOsc.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "ULTOSC", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_dx(self, event: Union[str, dict]) -> Quote:
        """returns the directional movement index (DX) values.
        
        See also: http://www.investopedia.com/articles/technical/02/050602.asp
                : http://www.fmlabs.com/reference/default.htm?url=DX.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "DX",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_minus_di(self, event: Union[str, dict]) -> Quote:
        """returns the minus directional indicator (MINUS_DI) values.
        
        See also: http://www.investopedia.com/articles/technical/02/050602.asp
                : http://www.fmlabs.com/reference/default.htm?url=DI.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MINUS_DI",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_plus_di(self, event: Union[str, dict]) -> Quote:
        """returns the plus directional indicator (PLUS_DI) values.
        
        See also: http://www.investopedia.com/articles/technical/02/050602.asp
                : http://www.fmlabs.com/reference/default.htm?url=DI.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "PLUS_DI",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_minus_dm(self, event: Union[str, dict]) -> Quote:
        """returns the minus directional movement (MINUS_DM) values.
        
        See also: http://www.investopedia.com/articles/technical/02/050602.asp

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MINUS_DM",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_plus_dm(self, event: Union[str, dict]) -> Quote:
        """returns the plus directional movement (PLUS_DM) values.
    
        See also: http://www.investopedia.com/articles/technical/02/050602.asp

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "PLUS_DM",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_bbands(self, event: Union[str, dict]) -> Quote:
        """returns the Bollinger bands (BBANDS) values.
        
        See also: http://www.investopedia.com/articles/technical/04/030304.asp
                : http://www.fmlabs.com/reference/default.htm?url=Bollinger.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "BBANDS",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_midpoint(self, event: Union[str, dict]) -> Quote:
        """returns the midpoint (MIDPOINT) values. MIDPOINT = (highest value + lowest value)/2.
        

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MIDPOINT",
            "interval": "daily",
            "time_period": "60",
            "series_type": "close",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_midprice(self, event: Union[str, dict]) -> Quote:
        """returns the midpoint price (MIDPRICE) values. MIDPRICE = (highest high + lowest low)/2.
        

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "MIDPRICE",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_sar(self, event: Union[str, dict]) -> Quote:
        """returns the parabolic SAR (SAR) values. See also: Investopedia article and mathematical reference.
        

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "SAR", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_trange(self, event: Union[str, dict]) -> Quote:
        """returns the true range (TRANGE) values.
        
        See also: http://www.fmlabs.com/reference/default.htm?url=TR.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "TRANGE", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_atr(self, event: Union[str, dict]) -> Quote:
        """returns the average true range (ATR) values.
        
        See also: http://www.investopedia.com/articles/trading/08/average-true-range.asp
                : http://www.fmlabs.com/reference/default.htm?url=ATR.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "ATR",
            "interval": "daily",
            "datatype": "json",
            "time_period": "60",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_natr(self, event: Union[str, dict]) -> Quote:
        """returns the normalized average true range (NATR) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "NATR",
            "interval": "daily",
            "time_period": "60",
            "datatype": "json",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ad(self, event: Union[str, dict]) -> Quote:
        """returns the Chaikin A/D line (AD) values.
        
        See also: http://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp
                : http://www.fmlabs.com/reference/default.htm?url=AccumDist.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "AD", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_adosc(self, event: Union[str, dict]) -> Quote:
        """returns the Chaikin A/D oscillator (ADOSC) values.
        
        See also: http://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp
                : http://www.fmlabs.com/reference/default.htm?url=AccumDist.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "ADOSC", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_obv(self, event: Union[str, dict]) -> Quote:
        """returns the on balance volume (OBV) values.
        
        See also: http://www.investopedia.com/articles/technical/100801.asp
                : http://www.fmlabs.com/reference/default.htm?url=OBV.htm

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {"function": "OBV", "interval": "daily", "datatype": "json"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_trendline(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, instantaneous trendline (HT_TRENDLINE) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_TRENDLINE",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_sine(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, sine wave (HT_SINE) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_SINE",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_trendmode(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, trend vs cycle mode (HT_TRENDMODE) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_TRENDMODE",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_dcperiod(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, dominant cycle period (HT_DCPERIOD) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_DCPERIOD",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_dcphase(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, dominant cycle period (HT_DCPERIOD) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_DCPHASE",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)

    def get_ht_phasor(self, event: Union[str, dict]) -> Quote:
        """returns the Hilbert transform, phasor components (HT_PHASOR) values.

        Args:
            event: A ticker symbol str OR dict of parameters to be sent to the API

        Returns: Quote

        """
        defaults = {
            "function": "HT_PHASOR",
            "interval": "daily",
            "datatype": "json",
            "series_type": "close",
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.model_validate(json_response)
