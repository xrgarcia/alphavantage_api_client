# alphavantage-api-client
I use these functions in my AWS Step function statemachines. Each method for querying stock data has 2 params (event,context).
This will support AWS lambda functions, but also allow you to use it any way your want!
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



