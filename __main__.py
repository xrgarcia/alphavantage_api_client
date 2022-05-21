#from alphavantage_api_client.client import AlphavantageClient
import json
import subprocess
def main():
    event = {
        "symbol": "TSLA"
    }
    result = {}
    #client = AlphavantageClient().with_api_key('[you key here]')
    # result['overview'] = client.get_company_overview(event)
    # result['latest_stock_price'] = client.get_latest_stock_price(event)
    # result['stock_price'] = client.get_stock_price(event)
    # result['earnings'] = client.get_earnings(event)
    # result['latest_earnings'] = client.get_latest_earnings(event)
    # result['cash_flow'] = client.get_cash_flow(event)
    # result['latest_cash_flow'] = client.get_latest_cash_flow(event)
    # result['income_statement'] = client.get_income_statement_for_symbol(event)
    #result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
    #print(json.dumps(result))
    alphavantage_api_client_version = subprocess.run(['git', 'describe', '--tags'],
                                                     stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    print(alphavantage_api_client_version)
if __name__ == "__main__":
    main()


