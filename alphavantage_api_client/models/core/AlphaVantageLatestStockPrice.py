from pydantic import BaseModel, Field

from alphavantage_api_client.models.alphavantage.GlobalQuote import GlobalQuote


class AlphaVantageLatestStockPrice(BaseModel):
    global_quote: GlobalQuote = Field(..., alias='Global Quote')

    def __init__(self, global_quote: GlobalQuote):
        self.global_quote = global_quote
