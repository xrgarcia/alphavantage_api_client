from alphavantage_api_client import AlphavantageClient
import json
import os
from os.path import exists


class MockAlphavantageClient(AlphavantageClient):

    def __init__(self):
        super().__init__()
        path = os.getcwd()
        self.base_path = f"{path}/tests/mocks"
        if not exists(self.base_path):
            self.base_path = f"{path}/alphavantage_api_client/tests/mocks"

    def get_data_from_alpha_vantage(self, event, context=None):
        '''
        Get all data from alpha vantage
        :param event:
        :param context:
        :return:
        :rtype: dict
        '''
        if event is None:
            raise ValueError("Event property isn't define")

        text_file = None
        if event.get("function") == "GLOBAL_QUOTE":
            text_file = open(f"{self.base_path}/mock_stock_quote.json", "r")
        elif event.get("function") == "BALANCE_SHEET":
            text_file = open(f"{self.base_path}/mock_balance_sheet.json", "r")
        elif event.get("function") == "INCOME_STATEMENT":
            text_file = open(f"{self.base_path}/mock_income_statement.json", "r")
        elif event.get("function") == "CASH_FLOW":
            text_file = open(f"{self.base_path}/mock_cash_flow.json", "r")
        elif event.get("function") == "EARNINGS":
            text_file = open(f"{self.base_path}/mock_earnings.json", "r")
        elif event.get("function") == "OVERVIEW":
            text_file = open(f"{self.base_path}/mock_company_profile.json", "r")
        elif event.get("function") == "CRYPTO_INTRADAY" and event.get("outputsize") == "full":
            text_file = open(f"{self.base_path}/mock_crypto_full.json", "r")
        elif event.get("function") == "REAL_GDP":
            text_file = open(f"{self.base_path}/mock_real_gdp.json", "r")
        elif event.get("function") == "EMA":
            text_file = open(f"{self.base_path}/mock_technical_indicator_ema.json")
        elif event.get("function") == "SMA":
            text_file = open(f"{self.base_path}/mock_technical_indicator_sma_equity.json", "r")
        elif event.get("function") == "TIME_SERIES_DAILY" and event.get("outputsize") == "compact":
            text_file = open(f"{self.base_path}/mock_stock_price_full.json", "r")
        elif event.get("function") == "TIME_SERIES_INTRADAY" and event.get("interval") == "5min":
            text_file = open(f"{self.base_path}/mock_intraday_series_quote.json", "r")
        else:
            raise ValueError(f"We don't have a mock data file for your request {json.dumps(event)}")

        data = text_file.read()
        text_file.close()
        json_response = json.loads(data)
        json_response["success"] = True
        json_response["limit_reached"] = False
        json_response["status_code"] = 200
        if "symbol" in event:
            json_response["symbol"] = event["symbol"]
        return json_response
