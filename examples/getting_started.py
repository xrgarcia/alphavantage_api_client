from alphavantage_api_client import AlphavantageClient, GlobalQuote, AccountingReport


def sample_get_stock_price():
    client = AlphavantageClient()
    event = {
        "symbol": "TSLA"
    }
    global_quote = client.get_global_quote(event)
    if not global_quote.success:
        raise ValueError(f"{global_quote.error_message}")
    print(global_quote.json())  # convenience method that will convert to json
    print(f"stock price: ${global_quote.get_price()}")  # convenience method to get stock price
    print(f"trade volume: {global_quote.get_volume()}")  # convenience method to get volume
    print(f"low price: ${global_quote.get_low_price()}")  # convenience method to get low price for the day


def sample_accounting_reports():
    client = AlphavantageClient()
    event = {
        "symbol": "TSLA"
    }
    earnings = client.get_earnings(event)
    cash_flow = client.get_cash_flow(event)
    balance_sheet = client.get_balance_sheet(event)
    income_statement = client.get_income_statement(event)

    print(earnings.json())
    print(cash_flow.json())
    print(balance_sheet.json())
    print(income_statement.json())

    reports = [earnings,cash_flow, balance_sheet, income_statement]

    # show that each report is in the same type and how to access the annual and quarterly reports
    for accounting_report in reports:
        print(accounting_report.quarterlyReports) # array of  all quarterly report
        print(accounting_report.annualReports) # array of all annual reports
        print(accounting_report.get_most_recent_annual_report()) # get the most recent annual report
        print(accounting_report.get_most_recent_quarterly_report()) # get the most recent quarterly report;


if __name__ == "__main__":
    sample_accounting_reports()
