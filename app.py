import logging

from alphavantage_api_client import AlphavantageClient
import json

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    event = {
        "symbol": "TSLA"
    }
    result = {}
    client = AlphavantageClient()
    global_quote = client.get_global_quote(event)
    print(global_quote.json())
