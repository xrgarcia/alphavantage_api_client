import requests
import os
import configparser


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
            for stock_date in result[time_series_key]:
                latest_stock_price = result[time_series_key][stock_date]
                break

            # set latest stock data to root
            result["fetch_date"] = latest_stock_date
            for key in latest_stock_price:
                result[key] = latest_stock_price[key]
            # delete extra data
            result.pop(time_series_key)
            result.pop(meta_key)
        return result

    def get_stock_price(self, event, context=None):
        '''

        :param event:
        :param context:
        :return:
        '''
        if "symbol" not in event:
            raise ValueError("You must pass in symbol to get stock price")
        req = {
            "symbol": event['symbol'],
            "datatype": "json"
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

    def get_stock_price_from_alpha_vantage(self, event, context=None):
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

    def has_reached_limit(self, response):
        if "Note" in response and " calls per minute " in response["Note"]:
            return True
        else:
            return False

    def get_data_from_alpha_vantage(self, event, context=None):
        url = f'https://www.alphavantage.co/query?'
        # get api key if not provided
        if 'apikey' not in event:
            event["apikey"] = self.__api_key__
        if event["apikey"] == None or len(event["apikey"]) == 0:
            raise ValueError(
                "You must call client.with_api_key([api_key]), create config file in your profile (i.e. ~/.alphavantage) or event[api_key] = [your api key] before retrieving data from alphavantage")

        # default dataType is json
        if "datatype" not in event:
            event["datatype"] = "json"

        # build url from event
        for property in event:
            url += f'{property}={event[property]}&'
        url = url[:-1]
        # fetch data from API
        r = requests.get(url)

        requested_data = {
            "limit_reached": False,
            "success": False
        }
        # verify request worked correctly and build response
        # gotta check if consumer request json or csv, so we can parse the output correctly
        # todo need to parse csv data for errors, for now we can just a pass through

        # check for CSV data type and successful response
        if len(r.text) > 0 and r.status_code == 200 and 'datatype' in event and event["datatype"] == 'csv' \
                and "Error Message" not in r.text:
            requested_data['csv'] = r.text
            requested_data['success'] = True
        # check for failed json response
        elif 'datatype' in event and event["datatype"] == 'json' and (
                len(r.text) == 0 or r.text == "{}" or "Error Message" in r.text or self.has_reached_limit(r.json())):
            requested_data['status_code'] = r.status_code
            json_response = r.json()
            if self.has_reached_limit(json_response):
                requested_data['limit_reached'] = True
                requested_data['Error Message'] = json_response["Note"]
            if "Error Message" in json_response:
                requested_data['Error Message'] = json_response["Error Message"]
            if "Information" in json_response:
                requested_data['Error Message'] = json_response["Information"]
            if len(json_response) == 0:
                requested_data['Error Message'] = "Symbol not found"
            requested_data['success'] = False
        # check for successfully json response
        elif 'datatype' in event and event["datatype"] == 'json' and len(
                r.text) > 0 and r.text != "{}" and "Error Message" not in r.text and not self.has_reached_limit(
            r.json()):
            json_response = r.json()
            for field in json_response:
                requested_data[field] = json_response[field]


            if len(requested_data) > 0:
                requested_data['success'] = True
            else:
                requested_data['success'] = False
        # assume failure
        else:
            requested_data['Error Message'] = r.text
            requested_data['success'] = False
        # if request has a symbol then publish in response
        if "symbol" in event:
            requested_data['symbol'] = event['symbol']

        return requested_data
