import requests
from client import AlphavantageClient




if __name__ == "__main__":
    event = {
        "symbol":"TSLA"
    }

    client = AlphavantageClient()
    result = client.get_company_overview(event)
    print(result)

