from typing import Optional
from alphavantage_api_client import AlphavantageClient, GlobalQuote, Quote, CompanyOverview, AccountingReport
from time import sleep


class Ticker:

    def __init__(self):
        self.__client__: AlphavantageClient = None
        self.__symbol__: str = None
        self.__global_quote__: GlobalQuote = None
        self.__intraday_quote__: Quote = None
        self.__earnings__: AccountingReport = None
        self.__income_statement__: AccountingReport = None
        self.__company_overview__: CompanyOverview = None
        self.__retry_when_limit_reached__ = False

    def create_client(self, api_key: str = None):
        if not api_key:
            self.__client__ = AlphavantageClient()
        else:
            self.__client__ = AlphavantageClient().with_api_key(api_key)

        return self

    def get_client(self):
        return self.__client__

    def use_client(self, client: AlphavantageClient = None):
        if not client or client is None:
            raise ValueError("You must define a client before i can use it.")

        self.__client__ = client

        return self

    def from_symbol(self, symbol: str = None):
        if symbol is None or not symbol or len(symbol) == 0:
            raise ValueError("symbol must be defined")

        self.__symbol__ = symbol

        return self

    def should_retry_once(self, retry_status: bool = True):
        self.__client__.should_retry_once(retry_status)

        return self

    def fetch_global_quote(self):
        event = {
            "symbol": self.__symbol__
        }
        self.__global_quote__ = self.__client__.get_global_quote(event)

        return self

    def fetch_income_statement(self):
        event = {
            "symbol": self.__symbol__
        }
        self.__income_statement__ = self.__client__.get_income_statement(event)

        return self

    def fetch_earnings(self):
        event = {
            "symbol": self.__symbol__
        }
        self.__earnings__ = self.__client__.get_earnings(event)

        return self

    def fetch_company_overview(self):
        event = {
            "symbol": self.__symbol__
        }
        self.__company_overview__ = self.__client__.get_company_overview(event)

        return self

    def fetch_intraday_quote(self):
        event = {
            "symbol": self.__symbol__
        }
        intraday_quote = self.__client__.get_intraday_quote(event)
        self.__intraday_quote__ = intraday_quote
        return self

    def get_global_quote(self) -> GlobalQuote:
        if self.__global_quote__ is None or not self.__global_quote__:
            raise ValueError("global_quote is not defined. You call fetch_global_quote(...) to populate it")
        return self.__global_quote__

    def get_intraday_quote(self) -> Quote:
        if self.__intraday_quote__ is None or not self.__intraday_quote__:
            raise ValueError("intraday_quote is not defined. You call fetch_intraday_quote(...) to populate it")
        return self.__intraday_quote__

    def get_company_overview(self) -> Quote:
        if self.__company_overview__ is None or not self.__company_overview__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__company_overview__

    def get_earnings(self) -> AccountingReport:
        if self.__earnings__ is None or not self.__earnings__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__earnings__

    def get_income_statement(self) -> AccountingReport:
        if self.__income_statement__ is None or not self.__income_statement__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__income_statement__
