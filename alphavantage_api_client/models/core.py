from pydantic import BaseModel, Field
from typing import Optional
import re


class BaseResponse(BaseModel):
    success: bool
    limit_reached: bool
    status_code: int
    error_message: Optional[str] = Field(None, alias='Error Message')
    data: Optional[dict]
    csv: Optional[str]
    symbol: Optional[str]


class BaseQuote(BaseResponse):
    symbol: str


class BaseIntradayQuote(BaseQuote):
    meta_data: Optional[dict] = Field(None, alias='Meta Data')


class GlobalQuote(BaseQuote):
    data: Optional[dict] = Field({}, alias='Global Quote')


def gen_crypto_intraday_alias(field_name):
    new_field_name = field_name
    if field_name.startswith('Time Series Crypto ('):
        new_field_name = "data"

    return new_field_name


class CryptoIntradayQuote(BaseIntradayQuote):
    data: Optional[dict] = Field(None, alias='data')
    class Config:
        alias_generator = gen_crypto_intraday_alias
        allow_population_by_field_name = True
