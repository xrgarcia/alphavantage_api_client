import time

import requests
import os
import configparser
from .response_validation_rules import ValidationRuleChecks
import json
from alphavantage_api_client.models import GlobalQuote, Quote, AccountingReport, CompanyOverview, RealGDP, \
    CsvNotSupported, TickerSearch, MarketStatus
import copy
import logging
import hashlib
from typing import Optional, Union


class ApiKeyNotFound(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class AlphavantageClient:
    def __init__(self):
        self.__total_calls__ = 0
        self.__max_cache_size__ = 0
        self.__retry__ = False
        self.__first_successful_attempt__ = 0
        self.__use_cache__ = False
        self.__cache__ = {}
        # try to get api key from USER_PROFILE/.alphavantage
        alphavantage_config_file_path = f'{os.path.expanduser("~")}{os.path.sep}.alphavantage'
        msg = {"method": "__init__", "action": f"{alphavantage_config_file_path} config file found"}
        if os.path.exists(alphavantage_config_file_path):
            logging.info(json.dumps(msg))
            config = configparser.ConfigParser()
            config.read(alphavantage_config_file_path)
            self.__api_key__ = config['access']['api_key']
            return
        # try to get from an environment variable
        elif os.environ.get('ALPHAVANTAGE_API_KEY') is not None:
            self.__api_key__ = os.environ.get('ALPHAVANTAGE_API_KEY')
            msg["action"] = f"api key found from environment"
            logging.info(json.dumps(msg))
            return
        else:
            self.__api_key__ = ""

    def __build_url_from_args__(self, event: dict):
        """

        Args:
            event:

        Returns:
            :rtype: str
        """
        url = f'https://www.alphavantage.co/query?'
        # build url from event
        for property in event:
            url += f'{property}={event[property]}&'
        url = url[:-1]
        return url

    def __inject_values__(self, default_values: dict, dest_obj: dict):
        """

        Args:
            default_values:
            dest_obj:

        Returns:
            :rtype: None

        """
        # inject defaults for missing values
        for default_key in default_values:
            if default_key not in dest_obj or dest_obj[default_key] is None:
                dest_obj[default_key] = default_values[default_key]

    def __create_api_request_from__(self, defaults: dict, event: dict):
        """

        Args:
            defaults:
            event:

        Returns:
            :rtype: dict
        """
        if event is not None:
            json_request = event.copy()
        else:
            json_request = {}
        self.__inject_values__(defaults, json_request)

        return json_request

    def should_retry_once(self, retry: bool = True):
        self.__retry__ = retry

        return self

    def use_simple_cache(self, use_cache: bool = True, max_cache_size: int = 100):
        """
        First in First Out Cache
        Args:
            use_cache:
            max_cache_size: Max size of the cache.

        Returns:

        """
        self.__use_cache__ = use_cache
        self.__max_cache_size__ = max_cache_size

        return self

    def get_internal_metrics(self) -> dict:
        total_calls = self.__total_calls__
        retry = self.__retry__
        first_successful_attempt = self.__first_successful_attempt__
        metrics = {
            "total_calls": total_calls,
            "retry": retry,
            "first_successful_attempt": first_successful_attempt
        }
        return metrics

    def with_api_key(self, api_key: str):
        """Specify the API Key when you are storing it somewhere other than in ini file or environment variable

        When you are storing your api key somewhere other than ~/.alphavantage or ALPHAVANTAGE_API_KEY env variable
        Args:
            api_key (str): Your api key from alphavantage

        Returns:
            :rtype: AlphavantageClient
        """
        if api_key is None or len(api_key) == 0:
            raise ApiKeyNotFound("API Key is null or empty. Please specify a valid api key")
        self.__api_key__ = api_key

        return self

    def get_global_quote(self, event: Union[str, dict]) -> GlobalQuote:
        """ Lightweight access to obtain stock quote data

        A lightweight alternative to the time series APIs, this service returns the price and volume information
        for a token of your choice.
        Args:
            event (dict): A ``dict`` containing the parameters supported by the api.
            Minimum required value is ``symbol (str)``

        Returns:
            :rtype: GlobalQuote

        """
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        defaults = {
            "function": "GLOBAL_QUOTE"
        }
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return GlobalQuote.parse_obj(json_response)

    def get_daily_quote(self, event: dict) -> Quote:
        """
        This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily
        volume) of the global equity specified, covering 20+ years of historical data. If you are also interested in
        split/dividend-adjusted historical data, please use the Daily Adjusted API, which covers adjusted close values
        and historical split and dividend events.
        Args:
            event: dict, required

        Returns: Quote

        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_DAILY",
                    "outputsize": "compact"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_daily_adjusted_quote(self, event: dict) -> Quote:
        """
                This API returns raw (as-traded) daily open/high/low/close/volume values,
                daily adjusted close values, and historical split/dividend events of the global
                equity specified, covering 20+ years of historical data.
                Args:
                    event: dict, required

                Returns: Quote

                """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_DAILY_ADJUSTED",
                    "outputsize": "compact"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_weekly_quote(self, event: dict) -> Quote:
        """
                        This API returns weekly time series (last trading day of each week, weekly open,
                        weekly high, weekly low, weekly close, weekly volume) of the global equity
                        specified, covering 20+ years of historical data.
                        Args:
                            event: dict, required

                        Returns: Quote

                        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_WEEKLY",
                    "outputsize": "compact"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_weekly_adjusted_quote(self, event: dict) -> Quote:
        """
                        This API returns weekly adjusted time series (last trading day of each week, weekly open,
                        weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend)
                        of the global equity specified, covering 20+ years of historical data.
                        Args:
                            event: dict, required

                        Returns: Quote

                        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_WEEKLY_ADJUSTED"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_monthly_quote(self, event: dict) -> Quote:
        """
                        This API returns monthly time series (last trading day of each month, monthly open,
                        monthly high, monthly low, monthly close, monthly volume) of the global equity specified,
                        covering 20+ years of historical data.
                        Args:
                            event: dict, required

                        Returns: Quote

                        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_MONTHLY"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_monthly_adjusted_quote(self, event: dict) -> Quote:
        """
                        This API returns monthly time series (last trading day of each month, monthly open,
                        monthly high, monthly low, monthly close, monthly volume) of the global equity specified,
                        covering 20+ years of historical data.
                        Args:
                            event: dict, required

                        Returns: Quote

                        """
        # default params
        defaults = {"datatype": "json", "function": "TIME_SERIES_MONTHLY_ADJUSTED"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_intraday_quote(self, event: dict) -> Quote:
        """ Intraday time series data covering extended trading hours.

        This API returns intraday time series of the equity specified, covering extended trading hours where applicable
        (e.g., 4:00am to 8:00pm Eastern Time for the US market). The intraday data is derived from the Securities
        Information Processor (SIP) market-aggregated data. You can query both raw (as-traded) and
        split/dividend-adjusted intraday data from this endpoint.  This API returns the most recent 1-2 months of
        intraday data and is best suited for short-term/medium-term charting and trading strategy development.
        If you are targeting a deeper intraday history, please use the Extended Intraday API.
        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = ``str``

        Returns:
            :rtype: Quote

        """
        # default params
        defaults = {"symbol": None, "datatype": "json", "function": "TIME_SERIES_INTRADAY",
                    "interval": "60min", "slice": "year1month1",
                    "outputsize": "compact"}
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_income_statement(self, event: dict) -> AccountingReport:
        """
        This API returns the annual and quarterly income statements for the company of interest, with
        normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day
        a company reports its latest earnings and financials.

        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = ``str``

        Returns:
            :rtype: AccountingReport

        """

        defaults = {
            "function": "INCOME_STATEMENT",
            "datatype": "json"
        }
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.parse_obj(json_response)

    def get_balance_sheet(self, event: dict) -> AccountingReport:
        defaults = {
            "function": "BALANCE_SHEET",
            "datatype": "json"
        }
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)

        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.parse_obj(json_response)

    def get_cash_flow(self, event: dict) -> AccountingReport:
        """
        This API returns the annual and quarterly cash flow for the company of interest, with normalized fields
        mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports
        its latest earnings and financials.
        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = ``str``

        Returns:
            :rtype: AccountingReport

        """
        defaults = {
            "function": "CASH_FLOW",
            "datatype": "json"
        }
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.parse_obj(json_response)

    def get_earnings(self, event: Union[str, dict]) -> AccountingReport:
        """
        This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also
        includes analyst estimates and surprise metrics.

        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = ``str``

        Returns:
            :rtype: AccountingReport

        """
        defaults = {
            "function": "EARNINGS",
            "datatype": "json"
        }
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }

        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return AccountingReport.parse_obj(json_response)

    def get_company_overview(self, event: dict) -> CompanyOverview:
        """
        This API returns the company information, financial ratios, and other key metrics for the equity specified.
        Data is generally refreshed on the same day a company reports its latest earnings and financials.

        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = ``str``

        Returns:
            Return a CompanyOverview Object

        """
        defaults = {
            "function": "OVERVIEW"
        }
        event_dict = event
        if isinstance(event, str):
            event_dict = {
                "symbol": event
            }
        if event_dict.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event_dict)
        json_request = self.__create_api_request_from__(defaults, event_dict)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return CompanyOverview.parse_obj(json_response)

    def get_crypto_intraday(self, event: dict) -> Quote:
        """
        This API returns intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency
        specified, updated realtime.

        Args:
            event (dict): A Dictionary of parameters that will be passed to the api.
            Minimum required is ``symbol`` = (``str``)

        Returns:
            :rtype: Quote

        """
        defaults = {
            "function": "CRYPTO_INTRADAY",
            "interval": "5min",
            "market": "USD",
            "outputsize": "compact"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return Quote.parse_obj(json_response)

    def get_real_gdp(self, event: dict = None) -> RealGDP:
        """

        This API returns the annual and quarterly Real GDP of the United States.

        Args:
            event (dict): Not required. You can pass in any parameters supported by the api

        Returns:
            :rtype: RealGDP

        """
        defaults = {
            "function": "REAL_GDP",
            "interval": "annual",
            "datatype": "json"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return RealGDP.parse_obj(json_response)

    def get_technical_indicator(self, event: dict) -> Quote:
        """
        Default technical indicator is SMA. You can change this by passing in ``function`` = ``[your indicator]``

        Args:
            event (dict): Parameters supported by the API

        Returns:
            :rtype: Quote

        """
        defaults = {
            "function": "SMA",
            "interval": "monthly",
            "datatype": "json"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)
        json_response["indicator"] = event.get("function")

        return Quote.parse_obj(json_response)

    def get_data_from_alpha_vantage(self, event: dict, should_retry: bool = False) -> dict:
        """
        This is the underlying function that talks to alphavantage api.  Feel free to pass in any parameters supported
        by the api.  You will receive a dictionary with the response from the web api. In addition, you will obtain
        the ``success``, ``error_message`` and ``limit_reached`` fields.
        Args:
            event (dictionary): The url parameters supported by the web api

        Returns:
            :rtype: dict

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

        # not all calls will have a symbol in the call to alphavantage.... if so we can to capture it.
        if "symbol" in event:
            requested_data['symbol'] = event['symbol']

        # put into cache if allowed
        if self.__use_cache__:
            self.__put_item_into_cache__(loggable_event, requested_data)

        logging.info(json.dumps({"method": "get_data_from_alpha_vantage"
                                    , "action": "return_value", "data": requested_data, "event": loggable_event}))

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

    def __hydrate_request__(self, requested_data: dict, checks: ValidationRuleChecks, event: dict, should_retry: bool):
        # verify request worked correctly and build response
        # gotta check if consumer request json or csv, so we can parse the output correctly
        requested_data['success'] = checks.expect_successful_response().passed()  # successful csv response
        if not requested_data['success']:
            requested_data['Error Message'] = checks.get_error_message()
        requested_data['limit_reached'] = checks.expect_limit_not_reached().passed()
        requested_data['status_code'] = checks.get_status_code()

        if checks.expect_json_datatype().expect_successful_response().passed():  # successful json response
            json_response = checks.get_obj()
            for field in json_response:
                requested_data[field] = json_response[field]

        if checks.expect_csv_datatype().expect_successful_response().passed():  # successful csv response
            requested_data['csv'] = checks.get_obj()

    def __fetch_data__(self, checks: ValidationRuleChecks, event: dict, loggable_event: dict):
        url = self.__build_url_from_args__(event)
        r = requests.get(url)
        if self.__first_successful_attempt__ == 0:
            self.__first_successful_attempt__ = time.perf_counter()
        self.__total_calls__ += 1
        checks.with_response(r)
        logging.info(json.dumps({"method": "get_data_from_alpha_vantage", "action": "response_from_alphavantage"
                                    , "status_code": r.status_code, "data": r.text, "event": loggable_event}))

    def __validate_api_key__(self, checks: ValidationRuleChecks, event: dict):
        # get api key if not provided
        if checks.expect_api_key_in_event().failed():
            event["apikey"] = self.__api_key__  # assume they passed to builder method.
        elif self.__api_key__ is None or len(self.__api_key__) == 0 or "apikey" not in event \
                or not event.get("apikey"):  # consumer didn't tell me where to get api key
            raise ApiKeyNotFound(
                "You must call client.with_api_key([api_key]), create config file in your profile (i.e. ~/.alphavantage) or event[api_key] = [your api key] before retrieving data from alphavantage")

    def __sleep__(self):
        then = self.__first_successful_attempt__
        now = time.perf_counter()
        diff = 60 - (now - then)
        logging.info(f"sleeping for {diff} seconds")
        if diff < 0:
            diff = 60
        time.sleep(diff)

    def clear_cache(self):
        self.__cache__.clear()

        return self

    def search_ticker(self, event) -> TickerSearch:
        """
        We've got you covered! The Search Endpoint returns the best-matching symbols and market information based
        on keywords of your choice. The search results also contain match scores that provide you with the full
        flexibility to develop your own search and filtering logic.
        Args:
            event: dict

        Returns: TickerSearch

        """
        defaults = {
            "function": "SYMBOL_SEARCH",
            "datatype": "json"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return TickerSearch.parse_obj(json_response)

    def get_market_status(self) -> MarketStatus:
        """
        This endpoint returns the current market status (open vs. closed) of major trading venues for equities,
        forex, and cryptocurrencies around the world.
        Returns:

        """
        json_request = {
            "function": "MARKET_STATUS"
        }
        json_response = self.get_data_from_alpha_vantage(json_request, self.__retry__)

        return MarketStatus.parse_obj(json_response)