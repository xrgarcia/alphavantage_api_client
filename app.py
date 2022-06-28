from alphavantage_api_client import AlphavantageClient
import json

if __name__ == "__main__":
    print('------ start test --------')
    event = {
        "symbol": "TSLA"
    }
    result = {}
    client = AlphavantageClient()
    company_overview = client.get_company_overview(event)
    print(company_overview.json())
    global_quote = client.get_global_quote(event)
    print(global_quote.json())
    intraday_quote = client.get_intraday_quote(event)
    print(intraday_quote.json())
    earnings = client.get_earnings(event)
    print(earnings.json())
    cash_flow = client.get_cash_flow(event)
    print(cash_flow.json())
    print('------ complete test --------')
