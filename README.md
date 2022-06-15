# alpha vantage api client

Simple python wrapper around alpha vantage api
https://www.alphavantage.co/

See the alpha vantage api documentation
https://www.alphavantage.co/documentation/

Get your free api key here https://www.alphavantage.co/support/#api-key

**NOTE: Free API keys have a limit of 5 calls per min and max of 500 calls per day.**

The main value proposition for this client is to type the response, interpret success/failure and return consistent
data structures:

Notable fields:

1. success (true/false) flag into your response. You can log response into splunk or cloudwatch and know when something
   fails
2. limit_reached (true/false) flag into your response. You can know the difference between an error and reaching limit
   so you can pause processing until you api key is allowed to make more requests
3. error_message (str) response message from the api or this client with details on what went wrong and how to fix it

You can log your response into splunk or cloud watch to create SRE (sight reliability engineering)
dashboards to help you improve your stock market searches

## install from pip

```
pip install alphavantage_api_client
```

## Sample Usage Specifying Api Key in Client Builder

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient().with_api_key('[you key here]')
result['overview'] = client.get_company_overview(event)
result['stock_price'] = client.get_global_quote(event)
result['earnings'] = client.get_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['income_statement'] = client.get_income_statement(event)
print(json.dumps(result))
```

## Sample Usage Specifying Api Key in request event

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
        "symbol":"TSLA",
        "api_key":"[your api key here]"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['stock_price'] = client.get_global_quote(event)
result['earnings'] = client.get_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['income_statement'] = client.get_income_statement(event)
print(json.dumps(result))
```

## Sample Usage Specifying Api Key in ini file

### On mac/linux based machines run the following command BUT use your own API KEY

```
echo -e "[access]\napi_key=[your key here]" > ~/.alphavantage
```

### Now try the below

```
from alphavantage_api_client import AlphavantageClient
import json 

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['stock_price'] = client.get_global_quote(event)
result['earnings'] = client.get_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['income_statement'] = client.get_income_statement(event)
print(json.dumps(result))
```

## Sample Usage Specifying Api Key in environment variable

### On mac/linux based machines run the following command BUT use your own API KEY

```
export ALPHAVANTAGE_API_KEY=[your key here]
```

### Now try the below

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['stock_price'] = client.get_global_quote(event)
result['earnings'] = client.get_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['income_statement'] = client.get_income_statement(event)
print(json.dumps(result))
```

## Available Data

### Stock Price
```
from alphavantage_api_client import AlphavantageClient

event = {
   "symbol": "ibm",
   "interval": "5min"
}
client = AlphavantageClient()
results = client.get_intraday_quote(event)
assert results.success, "Success field is missing or False"
assert not results.limit_reached, "Limit reached is true but not hitting API"
assert results.symbol == event["symbol"], "Symbol from results don't match event"
assert len(results.meta_data) > 0, "Meta Data field is zero or not present"
assert len(results.data) > 0, "Time Series (5min) field is zero or not present"
print(f"json data{results.json()}")
```

### Company Overview
```
event = {
        "symbol": "IBM"
    }
    company_overview = client.get_company_overview(event)
    assert company_overview.success, "Success field is missing or False"
    assert not company_overview.limit_reached, "Limit reached is true but not hitting API"
    assert company_overview.symbol == event["symbol"], "Symbol from results don't match event"
    assert len(company_overview.ex_dividend_date), "ExDividendDate is missing or empty or None"
    assert len(company_overview.analyst_target_price), "analyst_target_price field is missing or empty or None"
    print(f"Successfully tested test_company_overview for {event['symbol']}")
```
### Get Economic indicators

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
   "function": "REAL_GDP"
}
real_gdp = client.get_real_gdp(event)
assert real_gdp.success, "Success field is missing or False"
assert not real_gdp.limit_reached, "Limit reached is true but not hitting API"
assert len(real_gdp.unit), "unit field is missing, empty or None"
assert len(real_gdp.data), "data field is missing, empty or None"
print(f"Successfully tested test_query_real_gdp")
```

### Quote Cryptocurrency

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
   "symbol": "ETH",
   "function": "CRYPTO_INTRADAY",
   "outputsize": "full"
}
intraday_quote = client.get_crypto_intraday(event)
assert intraday_quote.success, "Success field is missing or False"
assert not intraday_quote.limit_reached, "Limit reached is true but not hitting API"
assert intraday_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert len(intraday_quote.data), "data{} is empty but it should contain properties"
assert len(intraday_quote.meta_data), "meta_data{} is empty but it should contain properties"
print(f"Successfully tested test_quote_crypto for {event['symbol']}")
```

### Quote Technical Indicators

```
from alphavantage_api_client import AlphavantageClient
import json

event = {
   "symbol": "ibm",
   "function": "SMA"
}
quote = client.get_technical_indicator(event)
assert quote.success, "Success field is missing or False"
assert not quote.limit_reached, "Limit reached is true but not hitting API"
assert quote.symbol == event["symbol"], "Symbol from results don't match event"
assert len(quote.meta_data), "Meta Data field is missing, empty or None"
assert len(quote.data), "Technical Analysis: SMA field is missing, empty or None"
print(f"Successfully tested test_query_technical_indicator_sma for {event['symbol']}")
```