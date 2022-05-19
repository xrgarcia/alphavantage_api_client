import requests
from client import AlphavantageClient
import json



if __name__ == "__main__":
    event = {
        "symbol":"TSLA"
    }
    result = {}
    client = AlphavantageClient()
    #result['overview'] = client.get_company_overview(event)
    #result['latest_stock_price'] = client.get_latest_stock_price(event)
    #result['stock_price'] = client.get_stock_price(event)
    #result['earnings'] = client.get_earnings(event)
    result = client.get_latest_earnings(event)
    print(json.dumps(result))

