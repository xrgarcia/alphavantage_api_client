from pydantic import BaseModel, Field


class GlobalQuote(BaseModel):
    field_01__symbol: str = Field(..., alias='01. symbol')
    field_02__open: str = Field(..., alias='02. open')
    field_03__high: str = Field(..., alias='03. high')
    field_04__low: str = Field(..., alias='04. low')
    field_05__price: str = Field(..., alias='05. price')
    field_06__volume: str = Field(..., alias='06. volume')
    field_07__latest_trading_day: str = Field(..., alias='07. latest trading day')
    field_08__previous_close: str = Field(..., alias='08. previous close')
    field_09__change: str = Field(..., alias='09. change')
    field_10__change_percent: str = Field(..., alias='10. change percent')
