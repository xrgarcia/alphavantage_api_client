import requests
import os
import configparser
from .response_validation_rules import ValidationRuleChecks
import json
from .models.core import GlobalQuote, Quote, AccountingReport, CompanyOverview, RealGDP, CsvNotSupported
import copy


class ApiKeyNotFound(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class AlphavantageClient:

    def __init__(self):

        # try to get api key from USER_PROFILE/.alphavantage
        alphavantage_config_file_path = f'{os.path.expanduser("~")}{os.path.sep}.alphavantage'
        if os.path.exists(alphavantage_config_file_path) == True:
            # print(f'{alphavantage_config_file_path} config file found')
            config = configparser.ConfigParser()
            config.read(alphavantage_config_file_path)
            self.__api_key__ = config['access']['api_key']
            return
        # try to get from an environment variable
        elif os.environ.get('ALPHAVANTAGE_API_KEY') is not None:
            self.__api_key__ = os.environ.get('ALPHAVANTAGE_API_KEY')
            # print(f'api key found from environment')
            return
        else:
            self.__api_key__ = ""

    def __build_url_from_args__(self, event: dict):
        url = f'https://www.alphavantage.co/query?'
        # build url from event
        for property in event:
            url += f'{property}={event[property]}&'
        url = url[:-1]
        return url

    def __inject_default_values__(self, event: dict):
        if "datatype" not in event:
            event["datatype"] = "json"

    def __inject_values__(self, default_values: dict, dest_obj: dict):
        # inject defaults for missing values
        for default_key in default_values:
            if default_key not in dest_obj or dest_obj[default_key] is None:
                dest_obj[default_key] = default_values[default_key]

    def __create_api_request_from__(self, defaults: dict, event: dict):
        json_request = event.copy()
        self.__inject_values__(defaults, json_request)
        self.__inject_default_values__(json_request)
        return json_request

    def with_api_key(self, api_key: str):
        '''

        :param api_key:
        :return: AlphavantageClient
        :rtype: AlphavantageClient
        '''
        if api_key == None or len(api_key) == 0:
            raise ApiKeyNotFound("API Key is null or empty. Please specify a valid api key")
        self.__api_key__ = api_key

        return self

    def get_global_quote(self, event: dict):
        '''
        Global Quote function from Alpha Vantage
        :param event:
        :return: GlobalQuote
        :rtype: GlobalQuote
        '''
        defaults = {
            "function": "GLOBAL_QUOTE"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return GlobalQuote.parse_obj(json_response)

    def get_intraday_quote(self, event: dict):
        '''
        Time Servies Intraday function from Alpha Vantage
        :param event:
        :return: IntraDayQuote
        :rtype: Quote
        '''
        # default params
        defaults = {"symbol": None, "datatype": "json", "function": "TIME_SERIES_INTRADAY",
                    "interval": "60min", "slice": "year1month1",
                    "outputsize": "compact"}
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return Quote.parse_obj(json_response)

    def get_income_statement(self, event: dict):
        '''
        Income Statement for a given company
        :param event: dict
        :return: AccountingReport
        :rtype: AccountingReport
        '''

        defaults = {
            "function": "INCOME_STATEMENT",
            "datatype": "json"
        }
        if event.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event)
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return AccountingReport.parse_obj(json_response)

    def get_cash_flow(self, event: dict):
        '''

        :param event:
        :return: AccountingReport
        :rtype: AccountingReport
        '''
        defaults = {
            "function": "CASH_FLOW",
            "datatype": "json"
        }
        if event.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event)
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return AccountingReport.parse_obj(json_response)

    def get_earnings(self, event: dict):
        '''

        :param event:
        :return: AccountingReport
        :rtype: AccountingReport
        '''
        defaults = {
            "function": "EARNINGS",
            "datatype": "json"
        }
        if event.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event)
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return AccountingReport.parse_obj(json_response)

    def get_company_overview(self, event: dict):
        '''

        :param event:
        :return: CompanyOverview
        :rtype: CompanyOverview
        '''
        defaults = {
            "function": "OVERVIEW"
        }
        if event.get("datatype") == "csv":
            raise CsvNotSupported(defaults.get("function"), event)
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return CompanyOverview.parse_obj(json_response)

    def get_crypto_intraday(self, event: dict):
        '''

        :param event:
        :return: IntraDayQuote
        :rtype: Quote
        '''
        defaults = {
            "function": "CRYPTO_INTRADAY",
            "interval": "5min",
            "market": "USD",
            "outputsize": "compact"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return Quote.parse_obj(json_response)

    def get_real_gdp(self, event: dict):
        '''
        Real GDP
        :param event:
        :return: RealGDP
        :rtype: RealGDP
        '''
        defaults = {
            "function": "REAL_GDP",
            "interval": "annual",
            "datatype": "json"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)

        return RealGDP.parse_obj(json_response)

    def get_technical_indicator(self, event: dict):
        '''
        Default technical indicator is SMA. You can change this by passing in function=[your indicator]
        :param event:
        :return: IntraDayQuote
        :rtype: Quote
        '''
        defaults = {
            "function": "SMA",
            "interval": "monthly",
            "datatype": "json"
        }
        json_request = self.__create_api_request_from__(defaults, event)
        json_response = self.get_data_from_alpha_vantage(json_request)
        json_response["indicator"] = event.get("function")

        return Quote.parse_obj(json_response)

    def get_data_from_alpha_vantage(self, event: dict):
        '''
        You can query any data from alpha vantage
        :param event: The params from alpha vantage documentation
        :return: dict of return values
        :rtype: dict
        '''
        checks = ValidationRuleChecks().from_customer_request(event)
        # get api key if not provided
        if checks.expect_api_key_in_event().failed():
            event["apikey"] = self.__api_key__
        elif self.__api_key__ is None or len(self.__api_key__) == 0:  # consumer didn't tell me where to get api key
            raise ApiKeyNotFound(
                "You must call client.with_api_key([api_key]), create config file in your profile (i.e. ~/.alphavantage) or event[api_key] = [your api key] before retrieving data from alphavantage")

        # fetch data from API
        url = self.__build_url_from_args__(event)
        r = requests.get(url)
        checks.with_response(r)
        requested_data = {}

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

        # not all calls will have symbol in the call to alphavantage.... if so we can to capture it.
        if "symbol" in event:
            requested_data['symbol'] = event['symbol']

        return requested_data
