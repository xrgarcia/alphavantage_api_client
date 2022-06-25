# alpha vantage api client

**Simple python wrapper around alpha vantage api. This client implements the production readiness
of storing your api key safely and a consistent data model from the api. You can log your response into splunk or cloud
watch to create SRE (sight reliability engineering)
dashboards to help you improve your stock market searches**

You can find alpha vantage api here https://www.alphavantage.co/

See the alpha vantage api documentation https://www.alphavantage.co/documentation/

Get your free api key here https://www.alphavantage.co/support/#api-key

**NOTE: Free API keys have a limit of 5 calls per min and max of 500 calls per day.**

## Notable fields:

#### Base Fields

1. success (true/false) flag into your response. You can log response into splunk or cloudwatch and know when something
   fails
2. limit_reached (true/false) flag into your response. You can know the difference between an error and reaching limit
   so you can pause processing until you api key is allowed to make more requests
3. error_message (str) is the response message from the api or this client with details on what went wrong and how to
   fix it

#### GlobalQuote, Quote

1. data (dictionary) contains the information requested
2. meta_data (dictionary) data describing the data requested

#### AccountingReport

1. annualReports (list) contains the annual earnings or income statement data requested
2. quarterlyReports (list) contains the quarterly earnings or income statement data requested

#### CompanyOverview

All data from the company overview api query
is https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
you will get in the root object that is strongly typed and the based fields mentioned above.

#### RealGDP

1. name (str)
2. interval (str)
3. unit (str)
4. data (list) GDP data requested

## install from pip

```
pip install alphavantage_api_client
```

## Sample Usage Specifying Api Key in Client Builder

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

## Sample Usage Specifying Api Key in request event

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

## Sample Usage Specifying Api Key in ini file

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

## Sample Usage Specifying Api Key in environment variable

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

## Available Data

### Stock Price Now

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

### Stock Price over multiple days

```
from alphavantage_api_client import AlphavantageClient

event = {
   "symbol": "ibm",
   "interval": "5min"
}
client = AlphavantageClient()
intraday_quote = client.get_intraday_quote(event)
assert intraday_quote.success, "Success field is missing or False"
assert not intraday_quote.limit_reached, "Limit reached is true but not hitting API"
assert intraday_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert len(intraday_quote.meta_data) > 0, "Meta Data field is zero or not present"
assert len(intraday_quote.data) > 0, "Time Series (5min) field is zero or not present"
print(f"json data{intraday_quote.json()}")
```

### Company Overview

```
from alphavantage_api_client import AlphavantageClient

event = {
   "symbol": "IBM"
}
client = AlphavantageClient()
company_overview = client.get_company_overview(event)
assert company_overview.success, "Success field is missing or False"
assert not company_overview.limit_reached, "Limit reached is true but not hitting API"
assert company_overview.symbol == event["symbol"], "Symbol from results don't match event"
assert len(company_overview.ex_dividend_date), "ExDividendDate is missing or empty or None"
assert len(company_overview.analyst_target_price), "analyst_target_price field is missing or empty or None"
print(f"json data{company_overview.json()}")
```

### Get Economic indicators

```
from alphavantage_api_client import AlphavantageClient

event = {
   "function": "REAL_GDP"
}
client = AlphavantageClient()
real_gdp = client.get_real_gdp(event)
assert real_gdp.success, "Success field is missing or False"
assert not real_gdp.limit_reached, "Limit reached is true but not hitting API"
assert len(real_gdp.unit), "unit field is missing, empty or None"
assert len(real_gdp.data), "data field is missing, empty or None"
print(f"json data{real_gdp.json()}")
```

### Quote Cryptocurrency

```
from alphavantage_api_client import AlphavantageClient

event = {
   "symbol": "ETH",
   "function": "CRYPTO_INTRADAY",
   "outputsize": "full"
}
client = AlphavantageClient()
intraday_quote = client.get_crypto_intraday(event)
assert intraday_quote.success, "Success field is missing or False"
assert not intraday_quote.limit_reached, "Limit reached is true but not hitting API"
assert intraday_quote.symbol == event["symbol"], "Symbol from results don't match event"
assert len(intraday_quote.data), "data{} is empty but it should contain properties"
assert len(intraday_quote.meta_data), "meta_data{} is empty but it should contain properties"
print(f"json data{intraday_quote.json()}")
```

### Quote Technical Indicators

```
from alphavantage_api_client import AlphavantageClient

event = {
   "symbol": "ibm",
   "function": "SMA"
}
client = AlphavantageClient()
quote = client.get_technical_indicator(event)
assert quote.success, "Success field is missing or False"
assert not quote.limit_reached, "Limit reached is true but not hitting API"
assert quote.symbol == event["symbol"], "Symbol from results don't match event"
assert len(quote.meta_data), "Meta Data field is missing, empty or None"
assert len(quote.data), "Technical Analysis: SMA field is missing, empty or None"
print(f"json data{quote.json()}")
```

### Any Other Data Avaialble
See https://www.alphavantage.co/documentation/
The event{} dictionary will contain the url parameters exactly as specified in the documentation.  The response will include
the based fields and the exact response from the api. This is bypassing the normalization process, but might be useful
for you.
```
from alphavantage_api_client import AlphavantageClient
import json

event = {
    "function": "EMA"
}
client = MockAlphavantageClient()
results = client.get_data_from_alpha_vantage(event)
assert type(results) is dict, "Results object should be a dictionary"
assert len(results) > 0, "There should be data in the results"

print(f"json data{json.dumps(results)}")
```