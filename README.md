# Alpha Vantage API Client

## Our Mission

Create a simple python wrapper around [alpha vantage api](https://www.alphavantage.co/documentation/). Normalize responses so you have consistency across end points. Provide direct access to each end point so customers who already use the API can have the flexibility. Make it easy to debug, so users can track down issues quickly. 

- You can find alpha vantage here: https://www.alphavantage.co/
- See the alpha vantage api documentation: https://www.alphavantage.co/documentation/
- Get your free api key here: https://www.alphavantage.co/support/#api-key


## Overview
* [How to Install](https://github.com/xrgarcia/alphavantage_api_client#how-to-install)
* [Specify API Key](https://github.com/xrgarcia/alphavantage_api_client#specifying-api-key)
* [Obtain Stock Price](https://github.com/xrgarcia/alphavantage_api_client#obtain-stock-price)
* [Obtain Accouting / Financial Statements](https://github.com/xrgarcia/alphavantage_api_client#obtain-accounting-reports--financial-statements)
* [Debugging / Logging](https://github.com/xrgarcia/alphavantage_api_client#debugging--logging)
* [Retry / Cache](https://github.com/xrgarcia/alphavantage_api_client#retry-and-cache) (optimize your free account!)
* [Our Wiki](https://github.com/xrgarcia/alphavantage_api_client/wiki)

## How to Install

```
pip install alphavantage_api_client
```



# Specifying API Key
There are a few ways you include your API Key:
### 1. Within each request
```
from alphavantage_api_client import AlphavantageClient

client = AlphavantageClient()
event = {
   "symbol": "ibm",
   "interval": "5min",
   "apikey" : "[your key here]"
}
global_quote = client.get_global_quote(event)
assert global_quote.success, "Success field is missing or False"
assert not global_quote.limit_reached, "Limit reached is true but not hitting API"
assert global_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert "meta_data" not in global_quote, "Metadata should not be present since it's not in the api"
assert len(global_quote.data) > 0, "Data field is zero or not present"

print(f"Response data {global_quote.json()}")
```
### 2. Within the Client
```
from alphavantage_api_client import AlphavantageClient

client = AlphavantageClient().with_api_key("[your api key here]")
event = {
   "symbol": "ibm",
   "interval": "5min"
}
global_quote = client.get_global_quote(event)
assert global_quote.success, "Success field is missing or False"
assert not global_quote.limit_reached, "Limit reached is true but not hitting API"
assert global_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert "meta_data" not in global_quote, "Metadata should not be present since it's not in the api"
assert len(global_quote.data) > 0, "Data field is zero or not present"

print(f"Response data {global_quote.json()}")
```
### 3. Within a system environment variable
#### On mac/linux based machines run the following command BUT use your own API KEY

```
export ALPHAVANTAGE_API_KEY=[your key here]
```

#### Now try the below

```
from alphavantage_api_client import AlphavantageClient

client = AlphavantageClient()
event = {
   "symbol": "ibm",
   "interval": "5min"
}
global_quote = client.get_global_quote(event)
assert global_quote.success, "Success field is missing or False"
assert not global_quote.limit_reached, "Limit reached is true but not hitting API"
assert global_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert "meta_data" not in global_quote, "Metadata should not be present since it's not in the api"
assert len(global_quote.data) > 0, "Data field is zero or not present"

print(f"Response data {global_quote.json()}")
```
### 4. Within an ini file
#### On mac/linux based machines run the following command BUT use your own API KEY

```
echo -e "[access]\napi_key=[your key here]" > ~/.alphavantage
```

#### Now try the below

```
from alphavantage_api_client import AlphavantageClient

client = AlphavantageClient()
event = {
   "symbol": "ibm",
   "interval": "5min"
}
global_quote = client.get_global_quote(event)
assert global_quote.success, "Success field is missing or False"
assert not global_quote.limit_reached, "Limit reached is true but not hitting API"
assert global_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert "meta_data" not in global_quote, "Metadata should not be present since it's not in the api"
assert len(global_quote.data) > 0, "Data field is zero or not present"

print(f"Response data {global_quote.json()}")
```

## Obtain Stock Price

```
from alphavantage_api_client import AlphavantageClient, GlobalQuote


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


if __name__ == "__main__":
    sample_get_stock_price()

```
returns the following output
```
{"success": true, "limit_reached": false, "status_code": 200, "error_message": null, "csv": null, "symbol": "TSLA", "data": {"01. symbol": "TSLA", "02. open": "259.2900", "03. high": "262.4500", "04. low": "252.8000", "05. price": "256.6000", "06. volume": "177460803", "07. latest trading day": "2023-06-23", "08. previous close": "264.6100", "09. change": "-8.0100", "10. change percent": "-3.0271%"}}
stock price: $256.6000
trade volume: 177460803
low price: $252.8000

```

## Obtain Accounting Reports / Financial Statements
There are 4 different accounting reports:
* **Cash Flow** - A cash flow statement is a financial statement that provides information about the cash inflows and outflows of a company during a specific period of time. It helps investors understand how a company generates and uses cash. 
* **Balance Sheet** - a financial statement that provides a snapshot of a company's financial position at a specific point in time. It shows the company's assets, liabilities, and shareholders' equity.
* **Income Statement** - also known as a profit and loss statement or P&L statement, is a financial statement that provides an overview of a company's revenues, expenses, and net income or loss over a specific period of time. It is one of the key financial statements used by investors to assess a company's profitability and financial performance.
* **Earnings Statements** - An earnings statement, also known as an earnings report or earnings statement, is a financial statement that provides an overview of a company's revenue, expenses, and profit or loss for a specific period of time. It is commonly used by investors to evaluate a company's financial performance. 

```
from alphavantage_api_client import AlphavantageClient, GlobalQuote, AccountingReport

def sample_accounting_reports():
    client = AlphavantageClient()
    earnings = client.get_earnings("TSLA")
    cash_flow = client.get_cash_flow("TSLA")
    balance_sheet = client.get_balance_sheet("TSLA")
    income_statement = client.get_income_statement("TSLA")
    reports = [earnings,cash_flow, balance_sheet, income_statement]

    # show that each report is in the same type and how to access the annual and quarterly reports
    for accounting_report in reports:
        if not accounting_report.success:
            raise ValueError(f"{accounting_report.error_message}")
        print(accounting_report.json())
        print(accounting_report.quarterlyReports) # array of  all quarterly report
        print(accounting_report.annualReports) # array of all annual reports
        print(accounting_report.get_most_recent_annual_report()) # get the most recent annual report
        print(accounting_report.get_most_recent_quarterly_report()) # get the most recent quarterly report;


if __name__ == "__main__":
    sample_accounting_reports()

```


## Debugging / Logging

### Debugging

We use the built in `import logging` library in python. Obtaining more information from the client behavior
is as simple as adjusting your log levels.

1. `logging.INFO` - This will get you json log statements (in case you put these into splunk or cloudwatch)
   that show which method is doing the work, the action, and the value or data is produced (where applicable).

   #### Example log showing where it found your API key

   ```
   {
     "method": "__init__",
     "action": "/home/[your user name]/.alphavantage config file found"
   }
   ```

   #### Example log during client.global_quote(...) call. The data property is the raw response from alpha vantage api:

   ```
   {
     "method": "get_data_from_alpha_vantage",
     "action": "response_from_alphavantage",
     "status_code": 200,
     "data": "{\n    \"Global Quote\": {\n        \"01. symbol\": \"TSLA\",\n        \"02. open\": \"712.4050\",\n        \"03. high\": \"738.2000\",\n        \"04. low\": \"708.2600\",\n        \"05. price\": \"737.1200\",\n        \"06. volume\": \"31923565\",\n        \"07. latest trading day\": \"2022-06-24\",\n        \"08. previous close\": \"705.2100\",\n        \"09. change\": \"31.9100\",\n        \"10. change percent\": \"4.5249%\"\n    }\n}"
   }
   ```

   #### Example log after converting response text into dictionary before returning to client:

   ```
   {
     "method": "get_data_from_alpha_vantage",
     "action": "return_value",
     "data": {
       "success": true,
       "limit_reached": false,
       "status_code": 200,
       "Global Quote": {
         "01. symbol": "TSLA",
         "02. open": "712.4050",
         "03. high": "738.2000",
         "04. low": "708.2600",
         "05. price": "737.1200",
         "06. volume": "31923565",
         "07. latest trading day": "2022-06-24",
         "08. previous close": "705.2100",
         "09. change": "31.9100",
         "10. change percent": "4.5249%"
       },
       "symbol": "tsla"
     }
   }
   ```

2. `logging.DEBUG` - This will get you all of the log statements from #1 and from the dependant libraries.
   #### Example:
   ```
   INFO:root:{"method": "__init__", "action": "/home/[your username]/.alphavantage config file found"}
   DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): www.alphavantage.co:443
   DEBUG:urllib3.connectionpool:https://www.alphavantage.co:443 "GET /query?symbol=tsla&function=GLOBAL_QUOTE&apikey=YRV1XL63GDIFS42A HTTP/1.1" 200 None
   INFO:root:{"method": "get_data_from_alpha_vantage", "action": "response_from_alphavantage", "status_code": 200, "data": "{\n    \"Global Quote\": {\n        \"01. symbol\": \"TSLA\",\n        \"02. open\": \"712.4050\",\n        \"03. high\": \"738.2000\",\n        \"04. low\": \"708.2600\",\n        \"05. price\": \"737.1200\",\n        \"06. volume\": \"31923565\",\n        \"07. latest trading day\": \"2022-06-24\",\n        \"08. previous close\": \"705.2100\",\n        \"09. change\": \"31.9100\",\n        \"10. change percent\": \"4.5249%\"\n    }\n}"}
   INFO:root:{"method": "get_data_from_alpha_vantage", "action": "return_value", "data": {"success": true, "limit_reached": false, "status_code": 200, "Global Quote": {"01. symbol": "TSLA", "02. open": "712.4050", "03. high": "738.2000", "04. low": "708.2600", "05. price": "737.1200", "06. volume": "31923565", "07. latest trading day": "2022-06-24", "08. previous close": "705.2100", "09. change": "31.9100", "10. change percent": "4.5249%"}, "symbol": "tsla"}}
   ```

## Retry and Cache

A free account only allows so many calls per min.  You can configure the client to use a simple cache and retry
if it detects your limit has been reached. This way you can get the most out of your free tier :-)
```
from alphavantage_api_client import AlphavantageClient, GlobalQuote

def sample_retry_when_limit_reached():
    client = AlphavantageClient().use_simple_cache().should_retry_once()
    symbols = ["TSLA","F","C","WFC","ZIM","PXD","PXD","POOL","INTC","INTU"] # more than 5 calls so should fail
    for symbol in symbols:
        event = {
            "symbol": symbol
        }
        global_quote = client.get_global_quote(event)
        if not global_quote.success:
            raise ValueError(f"{global_quote.error_message}")

        if global_quote.limit_reached:
            raise ValueError(f"{global_quote.error_message}")
        print(f"symbol: {global_quote.symbol}, Price: {global_quote.get_price()}, success {global_quote.success}")

    client.clear_cache() # when you are done making calls, clear cache
    
if __name__ == "__main__":
    sample_retry_when_limit_reached()

```
Produces output
```
symbol: TSLA, Price: 256.6000, success True
symbol: F, Price: 14.0200, success True
symbol: C, Price: 46.0200, success True
symbol: WFC, Price: 40.6100, success True
symbol: ZIM, Price: 12.1800, success True
symbol: PXD, Price: 198.6600, success True
symbol: PXD, Price: 198.6600, success True
symbol: POOL, Price: 352.3400, success True
symbol: INTC, Price: 33.0000, success True
symbol: INTU, Price: 452.6900, success True

Process finished with exit code 0
```

## More!

Check out our [wiki](https://github.com/xrgarcia/alphavantage_api_client/wiki) for more info!