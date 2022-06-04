# alphavantage-api-client

I use these functions in my AWS Step function statemachines. Each method for querying stock data has 2 params (
event,context).
This will support AWS lambda functions, but also allow you to use it any way your want!

At present alphavantage isn't great at Delineating failed messages (has reached limit, error or invalid symbol). This
client interprets the response and
injects two fields into your response:

1. success (true/false) flag into your response. You can log response into splunk or cloudwatch and know when something
   fails
2. limit_reached (true/false) flag into your response. You can know the difference between an error and reaching limit
   so you can pause processing until you api key is allowed to make more requests

## install from pip

```
pip install alphavantage_api_client
```

## Sample Usage Specifying Api Key in Client Builder

```
from alphavantage_api_client import AlphavantageClient

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient().with_api_key('[you key here]')
result['overview'] = client.get_company_overview(event)
result['latest_stock_price'] = client.get_latest_stock_price(event)
result['stock_price'] = client.get_stock_price(event)
result['earnings'] = client.get_earnings(event)
result['latest_earnings'] = client.get_latest_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['latest_cash_flow'] = client.get_latest_cash_flow(event)
result['income_statement'] = client.get_income_statement_for_symbol(event)
result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
print(json.dumps(result))
```

## Sample Usage Specifying Api Key in request event

```
from alphavantage_api_client import AlphavantageClient

event = {
        "symbol":"TSLA",
        "api_key":"[your api key here]"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['latest_stock_price'] = client.get_latest_stock_price(event)
result['stock_price'] = client.get_stock_price(event)
result['earnings'] = client.get_earnings(event)
result['latest_earnings'] = client.get_latest_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['latest_cash_flow'] = client.get_latest_cash_flow(event)
result['income_statement'] = client.get_income_statement_for_symbol(event)
result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
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

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['latest_stock_price'] = client.get_latest_stock_price(event)
result['stock_price'] = client.get_stock_price(event)
result['earnings'] = client.get_earnings(event)
result['latest_earnings'] = client.get_latest_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['latest_cash_flow'] = client.get_latest_cash_flow(event)
result['income_statement'] = client.get_income_statement_for_symbol(event)
result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
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

event = {
        "symbol":"TSLA"
}
result = {}
client = AlphavantageClient()
result['overview'] = client.get_company_overview(event)
result['latest_stock_price'] = client.get_latest_stock_price(event)
result['stock_price'] = client.get_stock_price(event)
result['earnings'] = client.get_earnings(event)
result['latest_earnings'] = client.get_latest_earnings(event)
result['cash_flow'] = client.get_cash_flow(event)
result['latest_cash_flow'] = client.get_latest_cash_flow(event)
result['income_statement'] = client.get_income_statement_for_symbol(event)
result['latest_income_statement'] = client.get_latest_income_statement_for_symbol(event)
print(json.dumps(result))
```

## Get any data from alphavantage using get_data_from_alpha_vantage(...)

### Get Economic indicators

```commandline
event = {
        "function": "REAL_GDP",
        "interval": "annual"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "success" in results and results[
        'success'] == True, "Success flag not present or equal to false when quoting real GDP"
    print(json.dumps(results))
    print("Can quote Real GDP")
```

### Quote Cryptocurrency

```commandline
event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "success" in results and results["success"] == True, f"Failed to receive a quote for {event['symbol']}"
    print(f"Successfully quoted cryptocurrency symbol {event['symbol']}")
```

### Quote Technical Indicators

```commandline
event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "success" in results and results[
        'success'] == True, "Success flag not present or equal to false when quoting IBM EMA technical indicator"
    print("Can quote IBM EMA technical indicator")
```