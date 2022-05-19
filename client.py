import requests
import os
import configparser

class AlphavantageClient:
    __api_key__ = ""

    def __init__(self):
        alphavantage_config_file_path = f'{os.path.expanduser("~")}{os.path.sep}.alphavantage'

        if os.path.exists(alphavantage_config_file_path) == True:
            print(f'{alphavantage_config_file_path} file found')
            config = configparser.ConfigParser()
            config.read(alphavantage_config_file_path)
            self.__api_key__ = config['access']['api_key']

    def with_api_key(self ,api_key):
        if api_key == None or len(api_key) == 0:
            raise ValueError("API Key is null or empty. Please specify a valid api key")
        self.__api_key__ = api_key

        return self

    def get_stock_price_for_symbol(self,event, context=None):
        if "symbol" not in event:
            raise ValueError("You must pass in symbol to get stock price")
        req = {
            "symbol": event['symbol']
        }
        json_response = self.get_stock_price_from_alpha_vantage(req)
        if json_response == None:
            json_response = {}
            json_response["1. open"] = None
            json_response["2. high"] = None
            json_response["3. low"] = None
            json_response["4. close"] = None
            json_response["5. volume"] = None
            json_response["report_date"] = None
            json_response["symbol"] = event["symbol"]
            # the success flag has already been set

        return json_response

    def get_income_statement_for_symbol(self, event=None, context=None):
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": event["symbol"]
        }
        stock_details = self.get_data_from_alpha_vantage(params)
        if "annualReports" in stock_details:
            annualReports = stock_details["annualReports"]
            for annualReport in annualReports:
                last_income_statement = annualReport
                for property in last_income_statement:
                    new_property = f'last_qrt_inc_stmt_{property}'
                    val = last_income_statement[property]
                    event[new_property] = val

                break

        event["income_statement"] = {
            "details": stock_details
        }

        return event

    def get_cash_flow_for_symbol(self, event=None, context=None):
        params = {
            "function": "CASH_FLOW",
            "symbol": event["symbol"]
        }
        return self.get_data_from_alpha_vantage(params)

    def get_earnings_for_symbol(self, event=None, context=None):
        event["function"] = "EARNINGS"
        params = {
            "function": "EARNINGS",
            "symbol": event["symbol"]
        }
        return self.get_data_from_alpha_vantage(params)

    def get_company_overview(self, event=None, context=None):
        event["function"] = "OVERVIEW"
        params = {
            "function": event["function"],
            "symbol": event["symbol"]
        }
        return self.get_data_from_alpha_vantage(params)

    def get_stock_price(self, event, context=None):
        # default params
        DEFAULTS = {"symbol": None, "datatype": "json", "function": "TIME_SERIES_DAILY",
                    "interval": "60min", "slice": "year1month1",
                    "outputsize": "compact"}
        json_request = {

        }
        # init the request from args
        for key in event:
            json_request[key] = event[key]
        # inject defaults for missing values
        for default_key in DEFAULTS:
            if default_key not in json_request or json_request[default_key] == None:
                json_request[default_key] = DEFAULTS[default_key]
        return self.get_data_from_alpha_vantage(json_request)

    def get_data_from_alpha_vantage(self, event, context=None):
        if self.__api_key__ == None or len(self.__api_key__) == 0:
            raise ValueError("You must call client.with_api_key([api_key]) or create config file in your profile (i.e. ~/.alphavantage) before retrieving data from alphavantage")

        url = f'https://www.alphavantage.co/query?'
        if 'apikey' not in event:
            event["apikey"] = self.__api_key__

        for property in event:
            url += f'{property}={event[property]}&'
        url = url[:-1]
        r = requests.get(url)
        requested_data = {

        }

        if r.status_code == 200 and 'datatype' in event and event["datatype"] == 'json' \
                and "Error Message" not in r.text:
            requested_data = r.json()
            requested_data['symbol'] = event['symbol']
            requested_data['success'] = True
        elif r.status_code == 200 and 'datatype' in event and event["datatype"] == 'csv' \
                and "Error Message" not in r.text:
            requested_data = r.text
            requested_data['success'] = True
        elif "Error Message" in r.text or "Information" in r.text:
            requested_data['status_code'] = r.status_code
            json_response = r.json()
            if "Error Message" in json_response:
                requested_data['Error Message'] = json_response["Error Message"]
            if "Information" in json_response:
                requested_data['Error Message'] = json_response["Information"]
            requested_data['success'] = False
        else:  # assume json
            requested_data = r.json()
            requested_data['symbol'] = event['symbol']
            requested_data['success'] = True

        return requested_data
