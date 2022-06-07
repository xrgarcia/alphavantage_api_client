import json
from alphavantage_api_client import AlphavantageClient
import time

def main():
    event = {
        "symbol": "AAPL"
        # ,"api_key":"your key here"
    }
    result = {}
    # your API key can be in ~/alphavantage ini file or in event['api_key'] = 'your key here'
    client = AlphavantageClient()
    result['overview'] = client.get_company_overview(event)
    result['latest_stock_price'] = client.get_latest_stock_price(event)
    result['stock_price'] = client.get_stock_price(event)
    result['earnings'] = client.get_earnings(event)
    result['latest_earnings'] = client.get_latest_earnings(event)
    time.sleep(60)
    result['cash_flow'] = client.get_cash_flow(event)
    result['latest_cash_flow'] = client.get_latest_cash_flow(event)
    result['income_statement'] = client.get_income_statement_for_symbol(event)
    result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
