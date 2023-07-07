import logging

from alphavantage_api_client import AlphavantageClient
import json

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    event = {
        "from_currency": "BTC",
        "to_currency": "CNY"
    }
    currency_quote = AlphavantageClient().get_crypto_exchange_rates(event)
    assert not currency_quote.limit_reached, f"limit_reached should not be true {currency_quote.error_message}"
    assert currency_quote.success, f"success is false {currency_quote.error_message}"
    assert len(currency_quote.data), "Data{} property is empty but should have information"
    logging.warning(
        f" Successfully quoted cryptocurrency symbol {event['from_currency']} to {event['to_currency']} in JSON")
