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
    if not company_overview.success:
        raise ValueError('Unable to get company overview')
    else:
        print(company_overview.json())

    global_quote = client.get_global_quote(event)
    if not global_quote.success:
        raise ValueError("Unable to get global quote")
    else:
        print(global_quote.json())

    intraday_quote = client.get_intraday_quote(event)
    if not intraday_quote.success:
        raise ValueError("Unable to get intraday quote")
    else:
        print(intraday_quote.json())

    earnings = client.get_earnings(event)
    if not earnings.success:
        raise ValueError("Unable to get earnings")
    else:
        print(earnings.json())

    cash_flow = client.get_cash_flow(event)
    if not cash_flow.success:
        raise ValueError("Unable to get Cashflow")
    else:
        print(cash_flow.json())
    print('------ complete test --------')
