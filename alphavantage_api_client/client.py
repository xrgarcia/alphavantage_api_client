import requests
import os
import configparser
from .response_validation_rules import ValidationRuleChecks
import json


class AlphavantageClient:
    __api_key__ = ""

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
        if os.environ.get('ALPHAVANTAGE_API_KEY') != None:
            self.__api_key__ = os.environ.get('ALPHAVANTAGE_API_KEY')
            # print(f'api key found from environment')
            return

    def with_api_key(self, api_key):
        if api_key == None or len(api_key) == 0:
            raise ValueError("API Key is null or empty. Please specify a valid api key")
        self.__api_key__ = api_key

        return self

    def get_latest_stock_price(self, event, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        time_series_key = "Time Series (Daily)"
        meta_key = "Meta Data"
        result = self.get_stock_price(event)
        # print(result)
        if result != None and result['success'] == True:
            latest_stock_price = {}
            latest_stock_date = result[meta_key]["3. Last Refreshed"]
            latest_stock_price = result[time_series_key][latest_stock_date]
            # set latest stock data to root
            result["fetch_date"] = latest_stock_date
            for key in latest_stock_price:
                result[key] = latest_stock_price[key]
            # delete extra data
            result.pop(time_series_key)
            result.pop(meta_key)
        return result

    def inject_values(self, default_values, dest_obj):
        # inject defaults for missing values
        for default_key in default_values:
            if default_key not in dest_obj or dest_obj[default_key] is None:
                dest_obj[default_key] = default_values[default_key]

    def get_stock_price(self, event, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        # default params
        DEFAULTS = {"symbol": None, "datatype": "json", "function": "TIME_SERIES_DAILY",
                    "interval": "60min", "slice": "year1month1",
                    "outputsize": "compact"}
        json_request = event.copy()
        self.inject_values(DEFAULTS, json_request)

        return self.get_data_from_alpha_vantage(json_request)

    def get_latest_income_statement_for_symbol(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": event["symbol"],
            "datatype": "json"
        }
        stock_details = self.get_data_from_alpha_vantage(params)
        if "annualReports" in stock_details:
            annualReports = stock_details["annualReports"]
            for annualReport in annualReports:
                last_income_statement = annualReport
                for property in last_income_statement:
                    new_property = f'annual_{property}'
                    val = last_income_statement[property]
                    stock_details[new_property] = val
                break
            stock_details.pop("annualReports")
        if "quarterlyReports" in stock_details:
            quarterlyReports = stock_details["quarterlyReports"]
            for quarterlyReport in quarterlyReports:
                last_income_statement = quarterlyReport
                for property in last_income_statement:
                    new_property = f'quarterly_{property}'
                    val = last_income_statement[property]
                    stock_details[new_property] = val
                break
            stock_details.pop("quarterlyReports")

        return stock_details

    def get_income_statement_for_symbol(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": event["symbol"],
            "datatype": "json"
        }
        stock_details = self.get_data_from_alpha_vantage(params)

        return stock_details

    def get_latest_cash_flow(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        result = self.get_cash_flow(event)
        if result != None and result['success'] == True and 'annualReports' in result and 'quarterlyReports' in result:
            annualReports = result['annualReports']
            if len(annualReports) > 0:
                first_annualReports = annualReports[0]
                for key in first_annualReports:
                    result[f'annual_{key}'] = first_annualReports[key]
                result.pop('annualReports')
            quarterlyReports = result['quarterlyReports']
            if len(quarterlyReports) > 0:
                first_quarterlyReports = quarterlyReports[0]
                for key in first_quarterlyReports:
                    result[f'quarterly_{key}'] = first_quarterlyReports[key]

                result.pop('quarterlyReports')

        return result

    def get_cash_flow(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        params = {
            "function": "CASH_FLOW",
            "symbol": event["symbol"],
            "datatype": "json"
        }
        return self.get_data_from_alpha_vantage(params)

    def get_latest_earnings(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        result = self.get_earnings(event)
        if result != None and result['success'] == True:
            annualEarnings = result['annualEarnings']
            if len(annualEarnings) > 0:
                first_annualEarnings = annualEarnings[0]
                for key in first_annualEarnings:
                    result[f'annual_{key}'] = first_annualEarnings[key]
                result.pop('annualEarnings')
            quarterlyEarnings = result['quarterlyEarnings']
            if len(quarterlyEarnings) > 0:
                first_quarterlyEarnings = quarterlyEarnings[0]
                for key in first_quarterlyEarnings:
                    result[f'quarterly_{key}'] = first_quarterlyEarnings[key]

                result.pop('quarterlyEarnings')

        return result

    def get_earnings(self, event=None, context=None):
        event["function"] = "EARNINGS"
        params = {
            "function": "EARNINGS",
            "symbol": event["symbol"],
            "datatype": "json"
        }
        return self.get_data_from_alpha_vantage(params)

    def get_company_overview(self, event=None, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        event["function"] = "OVERVIEW"
        params = {
            "function": event["function"],
            "symbol": event["symbol"],
            "datatype": "json"
        }
        return self.get_data_from_alpha_vantage(params)

    def __build_url_from_args(self, event):
        url = f'https://www.alphavantage.co/query?'
        # build url from event
        for property in event:
            url += f'{property}={event[property]}&'
        url = url[:-1]
        return url

    def inject_default_values(self, event):
        if "datatype" not in event:
            event["datatype"] = "json"

    def get_data_from_alpha_vantage(self, event, context=None):

        self.inject_default_values(event)
        checks = ValidationRuleChecks().from_customer_request(event)
        # get api key if not provided
        if checks.expect_api_key_in_event().failed():
            event["apikey"] = self.__api_key__
        elif self.__api_key__ is None or len(self.__api_key__) == 0:  # consumer didn't tell me where to get api key
            raise ValueError(
                "You must call client.with_api_key([api_key]), create config file in your profile (i.e. ~/.alphavantage) or event[api_key] = [your api key] before retrieving data from alphavantage")

        # fetch data from API
        url = self.__build_url_from_args(event)
        r = requests.get(url)
        checks.with_response(r)
        requested_data = {
            "limit_reached": False,
            "success": False
        }
        # verify request worked correctly and build response
        # gotta check if consumer request json or csv, so we can parse the output correctly
        # todo need to parse csv data for errors, for now we can just a pass through

        requested_data['success'] = checks.expect_successful_response().passed()  # successful csv response
        if not requested_data['success']:
            requested_data['Error Message'] = checks.get_error_message()
        requested_data['limit_reached'] = checks.expect_limit_not_reached().passed()
        requested_data['status_code'] = checks.get_status_code()
        if checks.expect_json_datatype().expect_successful_response().passed():  # successful json response
            json_response = checks.get_obj()
            for field in json_response:
                requested_data[field] = json_response[field]
        if checks.expect_csv_datatype().expect_successful_response().passed():
            requested_data['csv'] = checks.get_obj()
        if "symbol" in event:
            requested_data['symbol'] = event['symbol']

        return requested_data
