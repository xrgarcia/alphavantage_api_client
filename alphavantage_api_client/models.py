import pydantic
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
import copy


class CsvNotSupported(Exception):
    def __init__(self, function: str, event: dict):
        self.message = f"CSV Datatype is not supported by this function {function}"
        self.event = event
        super().__init__(self.message)


class BaseResponse(BaseModel):
    success: bool
    limit_reached: bool
    status_code: int
    error_message: Optional[str] = Field(None, alias='Error Message')
    csv: Optional[str] = None


class BaseQuote(BaseResponse):
    symbol: str


class TickerSearch(BaseResponse):
    data: list[dict] = Field({}, alias='bestMatches')

class MarketStatus(BaseResponse):
    endpoint: str
    data: list[dict] = Field({}, alias='markets')

class NewsAndSentiment(BaseResponse):
    items: int
    sentiment_score_definition: str
    relevance_score_definition: str
    data: list[dict] = Field({}, alias='feed')

class MarketMovers(BaseResponse):
    top_gainers: list[dict]
    top_losers: list[dict]
    last_updated: str
    meta_data: Optional[str] = Field(str, alias='metadata')
    most_actively_traded: list[dict]

class EarningsCalendarItem(BaseModel):
    symbol: str
    name: str
    report_date: str = Field(str,alias='reportDate')
    fiscal_date_ending: str = Field(str,alias='fiscalDateEnding')
    estimate: Optional[float] = None
    currency: Optional[str] = None

class IpoCalendarItem(BaseModel):
    symbol: str
    name: str
    ipo_date: str = Field(str,alias="ipoDate")
    price_range_low: Optional[float] = Field(float, alias="priceRangeLow")
    price_range_high: Optional[float] = Field(float, alias="priceRangeHigh")
    currency: Optional[str] = None
    exchange: Optional[str] = None

class IpoCalendar(BaseResponse):
    data: Optional[list[IpoCalendarItem]] = Field([])

class EarningsCalendar(BaseResponse):
    symbol: str
    data: Optional[list[EarningsCalendarItem]] = Field([])

class CurrencyQuote(BaseResponse):
    data: Optional[dict] = Field({})
    meta_data: Optional[dict] = Field({}, alias='Meta Data')

    @model_validator(mode="before")
    def normalize_fields(cls, values):
        return {
            "data" if k.startswith("Time Series FX (")
                      or k.startswith("Crypto Intraday (")
                      or k.startswith("Time Series Crypto (")
                      or k.startswith("Time Series (Digital Currency")
                      or k.startswith("Realtime Currency Exchange Rate") else k: v for k, v in values.items()
        }

class Commodity(BaseResponse):
    name: str
    interval: str
    unit: str
    data: list[dict]

class Quote(BaseQuote):
    """
    data is this clients abstraction of the response from alpha vantage. Time Series, Technical Indicator
    """
    data: Optional[dict] = {}
    meta_data: Optional[dict] = Field({}, alias='Meta Data')

    @model_validator(mode="before")
    def normalize_fields(cls, values):
        return {
            "data" if k.startswith("Weekly Adjusted Time Series")
                      or k.startswith("Monthly Adjusted Time Series")
                      or k.startswith("Monthly Time Series")
                      or k.startswith("Weekly Time Series")
                      or k.startswith("Technical Analysis: ")
                      or k.startswith("Time Series (")
                      or k.startswith("Time Series Crypto (") else k: v for k, v in values.items()
        }

    def get_most_recent_value(self) -> Optional[dict]:
        if len(self.data) > 0:
            for quote_date in self.data:
                quotes = self.data[quote_date]
                quotes["query_date"] = quote_date
                return quotes

        return None

    def get_oldest_value(self) -> Optional[dict]:
        if len(self.data) > 0:
            quote_dates = list(self.data.keys())
            last_quote_date = quote_dates[len(quote_dates) - 1]
            quote = self.data[last_quote_date]
            quote["query_date"] = last_quote_date

            return quote

        return None


class GlobalQuote(BaseQuote):
    data: dict = Field({}, alias='Global Quote')

    def get_open_price(self) -> str:
        field = "02. open"
        return self.get_data_value(field)

    def get_data_value(self, field) -> str:
        if field in self.data:
            return self.data[field]
        return None

    def get_high_price(self) -> str:
        field = "03. high"
        return self.get_data_value(field)

    def get_low_price(self) -> str:
        field = "04. low"
        return self.get_data_value(field)

    def get_price(self) -> str:
        field = "05. price"
        return self.get_data_value(field)

    def get_volume(self) -> str:
        field = "06. volume"
        return self.get_data_value(field)

    def get_latest_trading_day(self) -> str:
        field = "07. latest trading day"
        return self.get_data_value(field)

    def get_previous_close_day(self) -> str:
        field = "08. previous close"
        return self.get_data_value(field)

    def get_change_in_dollars(self) -> str:
        field = "09. change"
        return self.get_data_value(field)

    def get_change_percent(self) -> str:
        field = "10. change percent"
        return self.get_data_value(field)


class AccountingReport(BaseQuote):
    annualReports: list = Field(default=[], alias="annualReports")
    quarterlyReports: list = Field(default=[], alias="quarterlyReports")

    @model_validator(mode="before")
    def normalize_fields(cls, values):
        annual_report_fields = ["annualEarnings"]
        quarterly_report_fields = ["quarterlyEarnings"]
        new_values = copy.deepcopy(values)
        for field in new_values:
            new_field = field
            if field in annual_report_fields:
                new_field = "annualReports"
            elif field in quarterly_report_fields:
                new_field = "quarterlyReports"
            if new_field != field:
                values[new_field] = values[field]
                values.pop(field)
        return values

    def get_most_recent_annual_report(self) -> Optional[dict]:
        if len(self.annualReports) > 0:
            for index, annual_report in enumerate(self.annualReports):
                return annual_report

        return None

    def get_most_recent_quarterly_report(self) -> Optional[dict]:
        if len(self.quarterlyReports) > 0:
            for index, quarterly_report in enumerate(self.quarterlyReports):
                return quarterly_report

        return None


class EconomicIndicator(BaseResponse):
    name: Optional[str] = None
    interval: Optional[str] = None
    unit: Optional[str] = None
    data: Optional[list] = None


class CompanyOverview(BaseQuote):
    symbol: str = Field(default=None, alias='Symbol')
    asset_type: str = Field(default=None, alias='AssetType')
    name: str = Field(default=None, alias='Name')
    description: str = Field(default=None, alias='Description')
    central_index_key: str = Field(default=None, alias='CIK')
    exchange: str = Field(default=None, alias='Exchange')
    currency: str = Field(default=None, alias='Currency')
    country: str = Field(default=None, alias='Country')
    sector: str = Field(default=None, alias='Sector')
    Industry: str = Field(default=None, alias='Industry')
    address: str = Field(default=None, alias='Address')
    fiscal_year_end: str = Field(default=None, alias='FiscalYearEnd')
    latest_quarter: str = Field(default=None, alias='LatestQuarter')
    market_capitalization: str = Field(default=None, alias='MarketCapitalization')
    ebitda: str = Field(default=None, alias='EBITDA')
    pe_ratio: str = Field(default=None, alias='PERatio')
    pe_growth_ratio: str = Field(default=None, alias='PEGRatio')
    book_value: str = Field(default=None, alias='BookValue')
    dividend_per_share: str = Field(default=None, alias='DividendPerShare')
    dividend_yield: str = Field(default=None, alias='DividendYield')
    earnings_per_share: str = Field(default=None, alias='EPS')
    revenue_per_share_ttm: str = Field(default=None, alias='RevenuePerShareTTM')
    profit_margin: str = Field(default=None, alias='ProfitMargin')
    operating_margin_ttm: str = Field(default=None, alias='OperatingMarginTTM')
    return_on_assets_ttm: str = Field(default=None, alias='ReturnOnAssetsTTM')
    return_on_equity_ttm: str = Field(default=None, alias='ReturnOnEquityTTM')
    revenue_ttm: str = Field(default=None, alias='RevenueTTM')
    gross_profit_ttm: str = Field(default=None, alias='GrossProfitTTM')
    diluted_eps_ttm: str = Field(default=None, alias='DilutedEPSTTM')
    quarterly_earnings_growth_yoy: str = Field(default=None, alias='QuarterlyEarningsGrowthYOY')
    quarterly_revenue_growth_yoy: str = Field(default=None, alias='QuarterlyRevenueGrowthYOY')
    analyst_target_price: str = Field(default=None, alias='AnalystTargetPrice')
    trailing_pe: str = Field(default=None, alias='TrailingPE')
    forward_pe: str = Field(default=None, alias='ForwardPE')
    price_to_sales_ratio_ttm: str = Field(default=None, alias='PriceToSalesRatioTTM')
    price_to_book_ratio: str = Field(default=None, alias='PriceToBookRatio')
    ev_to_revenue: str = Field(default=None, alias='EVToRevenue')
    ev_to_ebitda: str = Field(default=None, alias='EVToEBITDA')
    beta: str = Field(default=None, alias='52WeekHigh')
    fifty_two_week_high: str = Field(default=None, alias='52WeekHigh')
    fifty_two_week_low: str = Field(default=None, alias='52WeekLow')
    fifty_day_moving_average: str = Field(default=None, alias='50DayMovingAverage')
    two_hundred_day_moving_average: str = Field(default=None, alias='200DayMovingAverage')
    shares_outstanding: str = Field(default=None, alias='SharesOutstanding')
    dividend_date: str = Field(default=None, alias='DividendDate')
    ex_dividend_date: str = Field(default=None, alias='ExDividendDate')

    def get_ex_dividend_date(self):
        """
        Alpha vantage api will return 'None' when there isn't an ex dividend date. This will return None or an ex
        dividend date.
        Returns:

        """
        if self.ex_dividend_date is None or len(self.ex_dividend_date) == 0 or "None" == self.ex_dividend_date:
            return None

        return self.ex_dividend_date
