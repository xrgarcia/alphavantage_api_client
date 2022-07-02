from alphavantage_api_client import AlphavantageClient
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    event = {
        "symbol": "tsla"
    }
    client = AlphavantageClient()

    global_quote = client.get_global_quote(event)
    assert global_quote.success, f"success was found to be {global_quote.success}: {global_quote.error_message}"
    assert global_quote.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not global_quote.limit_reached, f"{global_quote.error_message}"
    assert len(global_quote.data) > 0, "Response should have data but contains zero"
    logging.warning(f" Can quote stock symbol in JSON {event.get('symbol', None)}")
    logging.warning(global_quote.json())


if __name__ == "__main__":
    main()
