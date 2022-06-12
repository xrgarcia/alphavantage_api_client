from pydantic import BaseModel, Field
from typing import Optional


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
    csv: Optional[str]


class BaseQuote(BaseResponse):
    symbol: str


class Quote(BaseQuote):
    """
    data is this clients abstraction of the response from alpha vantage. Time Series, Technical Indicator
    """
    data: Optional[dict] = {}
    meta_data: Optional[dict] = Field({}, alias='Meta Data')


class GlobalQuote(BaseQuote):
    data: dict = Field({}, alias='Global Quote')


class AccountingReport(BaseQuote):
    annualReports: list = Field(..., alias="annualReports")
    quarterlyReports: list = Field(..., alias="quarterlyReports")


class RealGDP(BaseResponse):
    name: Optional[str]
    interval: Optional[str]
    unit: Optional[str]
    data: Optional[list]


class CompanyOverview(BaseQuote):
    symbol: str = Field(..., alias='Symbol')
    asset_type: str = Field(..., alias='AssetType')
    Name: str = Field(..., alias='Name')
    Description: str = Field(..., alias='Description')
    central_index_key: str = Field(..., alias='CIK')
    Exchange: str = Field(..., alias='Exchange')
    currency: str = Field(..., alias='Currency')
    country: str = Field(..., alias='Country')
    sector: str = Field(..., alias='Sector')
    Industry: str = Field(..., alias='Industry')
    address: str = Field(..., alias='Address')
    fiscal_year_end: str = Field(..., alias='FiscalYearEnd')
    latest_Quarter: str = Field(..., alias='LatestQuarter')
    market_capitalization: str = Field(..., alias='MarketCapitalization')
    ebitda: str = Field(..., alias='EBITDA')
    pe_ratio: str = Field(..., alias='PERatio')
    pe_growth_ratio: str = Field(..., alias='PEGRatio')
    book_value: str = Field(..., alias='BookValue')
    dividend_per_share: str = Field(..., alias='DividendPerShare')
    dividend_yield: str = Field(..., alias='DividendYield')
    earnings_per_share: str = Field(..., alias='EPS')
    revenue_per_share_ttm: str = Field(..., alias='RevenuePerShareTTM')
    profit_margin: str = Field(..., alias='ProfitMargin')
    operating_margin_ttm: str = Field(..., alias='OperatingMarginTTM')
    return_on_assets_ttm: str = Field(..., alias='ReturnOnAssetsTTM')
    return_on_equity_ttm: str = Field(..., alias='ReturnOnEquityTTM')
    revenue_ttm: str = Field(..., alias='RevenueTTM')
    gross_profit_ttm: str = Field(..., alias='GrossProfitTTM')
    diluted_eps_ttm: str = Field(..., alias='DilutedEPSTTM')
    quarterly_earnings_growth_yoy: str = Field(..., alias='QuarterlyEarningsGrowthYOY')
    quarterly_revenue_growth_yoy: str = Field(..., alias='QuarterlyRevenueGrowthYOY')
    analyst_target_price: str = Field(..., alias='AnalystTargetPrice')
    trailing_pe: str = Field(..., alias='TrailingPE')
    forward_pe: str = Field(..., alias='ForwardPE')
    price_to_sales_ratio_ttm: str = Field(..., alias='PriceToSalesRatioTTM')
    price_to_book_ratio: str = Field(..., alias='PriceToBookRatio')
    ev_to_revenue: str = Field(..., alias='EVToRevenue')
    ev_to_ebitda: str = Field(..., alias='EVToEBITDA')
    beta: str = Field(..., alias='52WeekHigh')
    fifty_two_week_high: str = Field(..., alias='52WeekHigh')
    fifty_two_week_low: str = Field(..., alias='52WeekLow')
    fifty_day_moving_average: str = Field(..., alias='50DayMovingAverage')
    two_hundred_day_moving_average: str = Field(..., alias='200DayMovingAverage')
    shares_outstanding: str = Field(..., alias='SharesOutstanding')
    dividend_date: str = Field(..., alias='DividendDate')
    ex_dividend_date: str = Field(..., alias='ExDividendDate')
