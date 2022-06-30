import logging

from alphavantage_api_client import AlphavantageClient
import json

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print('------ start test --------')
    event = {
        "symbol": "TSLA"
    }
    result = {}
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    print(json.dumps(results))
