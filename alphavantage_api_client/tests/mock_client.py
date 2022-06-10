from alphavantage_api_client import AlphavantageClient
import json
import os

class MockAlphavantageClient(AlphavantageClient):

    def get_data_from_alpha_vantage(self, event, context=None):
        if event is None:
            raise ValueError("Event property isn't define")
        path = os.getcwd()
        path = f"{path}/mocks"
        if event.get("function") == "GLOBAL_QUOTE":

            text_file = open(f"{path}/mock_stock_quote.json", "r")
            data = text_file.read()
            text_file.close()
            json_response = json.loads(data)
            json_response["success"] = True
            json_response["limit_reached"] = False
            json_response["status_code"] = 200
            json_response["symbol"] = event["symbol"]
            return json_response
