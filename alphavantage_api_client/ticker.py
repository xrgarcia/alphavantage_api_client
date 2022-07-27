import copy
from typing import Optional
from alphavantage_api_client import AlphavantageClient, GlobalQuote, Quote, CompanyOverview, AccountingReport
from time import sleep


class Ticker:

    def __init__(self):
        self.__client__: AlphavantageClient = None
        self.__symbol__: str = None
        self.__global_quote__: GlobalQuote = None
        self.__intraday_quote__: Quote = None
        self.__daily_quote__: Quote = None
        self.__earnings__: AccountingReport = None
        self.__cash_flow__: AccountingReport = None
        self.__balance_sheet__: AccountingReport = None
        self.__income_statement__: AccountingReport = None
        self.__company_overview__: CompanyOverview = None
        self.__retry_when_limit_reached__ = False
        self.__correlated_annual_reports__: dict[str, dict] = {}
        self.__correlated_quarterly_reports__: dict[str, dict] = {}
        self.__correlated_reports__: dict[str, dict] = {}

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

    def fetch_global_quote(self, params=None):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        if params is not None:
            self.__client__.__inject_values__(params, event)

        self.__global_quote__ = self.__client__.get_global_quote(event)

        return self

    def fetch_income_statement(self):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        self.__income_statement__ = self.__client__.get_income_statement(event)

        return self

    def fetch_earnings(self):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        self.__earnings__ = self.__client__.get_earnings(event)

        return self

    def fetch_cash_flow(self):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")

        event = {
            "symbol": self.__symbol__
        }
        self.__cash_flow__ = self.__client__.get_cash_flow(event)

        return self

    def fetch_company_overview(self):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        self.__company_overview__ = self.__client__.get_company_overview(event)

        return self

    def fetch_daily_quote(self, params=None):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        if params is not None:
            self.__client__.__inject_values__(params, event)

        daily_quote = self.__client__.get_intraday_quote(event)
        self.__daily_quote__ = daily_quote
        return self

    def fetch_intraday_quote(self, params=None):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        if params is not None:
            self.__client__.__inject_values__(params, event)

        intraday_quote = self.__client__.get_intraday_quote(event)
        self.__intraday_quote__ = intraday_quote
        return self

    def fetch_balance_sheet(self):
        if self.__symbol__ is None or len(self.__symbol__) == 0:
            raise ValueError("You must define the symbol by calling from_symbol(...)")
        event = {
            "symbol": self.__symbol__
        }
        self.__balance_sheet__ = self.__client__.get_balance_sheet(event)

        return self

    def fetch_accounting_reports(self):
        """
        This will fetch balance sheet, income statement and earnings from alphavantage api
        Returns:
            Ticker

        """
        self.fetch_balance_sheet().fetch_income_statement().fetch_earnings().fetch_cash_flow()

        return self

    def __rename_fields__(self, prefix, record: dict[str, object]):
        record_copy = copy.deepcopy(record)
        for key in record_copy:
            new_key = f"{prefix}{key}"
            record[new_key] = record[key]
            record.pop(key)

    def correlate_accounting_reports(self):
        earnings = self.get_earnings()
        balance_sheet = self.get_balance_sheet()
        income_statement = self.get_income_statement()
        cash_flow = self.get_cash_flow()
        self.correlate_accounting_report(earnings, "earnings_")
        self.correlate_accounting_report(balance_sheet, "balance_")
        self.correlate_accounting_report(income_statement, "income_")
        self.correlate_accounting_report(cash_flow, "cash_")
        for fiscal_ending_date in self.__correlated_quarterly_reports__:
            if fiscal_ending_date not in self.__correlated_reports__:
                self.__correlated_reports__[fiscal_ending_date] = \
                    self.__correlated_quarterly_reports__[fiscal_ending_date]
            else:
                report = self.__correlated_quarterly_reports__[fiscal_ending_date]
                self.__correlated_reports__[fiscal_ending_date].update(report)
        for fiscal_ending_date in self.__correlated_annual_reports__:
            if fiscal_ending_date not in self.__correlated_reports__:
                self.__correlated_reports__[fiscal_ending_date] = \
                    self.__correlated_annual_reports__[fiscal_ending_date]
            else:
                report = self.__correlated_annual_reports__[fiscal_ending_date]
                self.__correlated_reports__[fiscal_ending_date].update(report)

        return self

    def correlate_accounting_report(self, accounting_report: AccountingReport, prefix: str):
        for index, annual_report in enumerate(accounting_report.annualReports):
            fiscal_date_ending = annual_report.pop("fiscalDateEnding")
            self.__rename_fields__(f"{prefix}annual_", annual_report)
            annual_report["fiscalDateEnding"] = fiscal_date_ending
            if fiscal_date_ending not in self.__correlated_annual_reports__:
                self.__correlated_annual_reports__[fiscal_date_ending] = annual_report
            else:
                report = self.__correlated_annual_reports__[fiscal_date_ending]
                report.update(annual_report)

        for index, quarterly_report in enumerate(accounting_report.quarterlyReports):
            fiscal_date_ending = quarterly_report.pop("fiscalDateEnding")
            self.__rename_fields__(f"{prefix}quarterly_", quarterly_report)
            quarterly_report["fiscalDateEnding"] = fiscal_date_ending
            if fiscal_date_ending not in self.__correlated_quarterly_reports__:
                self.__correlated_quarterly_reports__[fiscal_date_ending] = quarterly_report
            else:
                report = self.__correlated_quarterly_reports__[fiscal_date_ending]
                report.update(quarterly_report)

    def get_correlated_annual_reports(self) -> dict[str, dict]:
        if self.__correlated_annual_reports__ is None \
                or not self.__correlated_annual_reports__ or len(self.__correlated_annual_reports__) == 0:
            raise ValueError("correlated_annual_reports is not defined. "
                             "You call correlate_accounting_reports(...) to populate it")
        return self.__correlated_annual_reports__

    def get_correlated_reports(self) -> dict[str, dict]:
        if self.__correlated_reports__ is None \
                or not self.__correlated_reports__ or len(self.__correlated_reports__) == 0:
            raise ValueError("correlated_reports is not defined. "
                             "You call correlate_accounting_reports(...) to populate it")
        return self.__correlated_reports__

    def get_correlated_quarterly_reports(self) -> dict[str, dict]:
        if self.__correlated_quarterly_reports__ is None \
                or not self.__correlated_quarterly_reports__ or len(self.__correlated_quarterly_reports__) == 0:
            raise ValueError("correlated_quarterly_reports is not defined. "
                             "You call correlate_accounting_reports(...) to populate it")
        return self.__correlated_quarterly_reports__

    def get_global_quote(self) -> GlobalQuote:
        if self.__global_quote__ is None or not self.__global_quote__:
            raise ValueError("global_quote is not defined. You call fetch_global_quote(...) to populate it")
        return self.__global_quote__

    def get_intraday_quote(self) -> Quote:
        if self.__intraday_quote__ is None or not self.__intraday_quote__:
            raise ValueError("intraday_quote is not defined. You call fetch_intraday_quote(...) to populate it")
        return self.__intraday_quote__

    def get_daily_quote(self) -> Quote:
        if self.__daily_quote__ is None or not self.__daily_quote__:
            raise ValueError("daily_quote is not defined. You call fetch_daily_quote(...) to populate it")
        return self.__daily_quote__

    def get_company_overview(self) -> CompanyOverview:
        if self.__company_overview__ is None or not self.__company_overview__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__company_overview__

    def get_cash_flow(self) -> Quote:
        if self.__cash_flow__ is None or not self.__cash_flow__:
            raise ValueError("cash_flow is not defined. You call fetch_cash_flow(...) to populate it")
        return self.__cash_flow__

    def get_earnings(self) -> AccountingReport:
        if self.__earnings__ is None or not self.__earnings__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__earnings__

    def get_income_statement(self) -> AccountingReport:
        if self.__income_statement__ is None or not self.__income_statement__:
            raise ValueError("company_overview is not defined. You call fetch_company_overview(...) to populate it")
        return self.__income_statement__

    def get_balance_sheet(self) -> AccountingReport:
        if self.__balance_sheet__ is None or not self.__balance_sheet__:
            raise ValueError("balance_sheet is not defined. You call fetch_balance_sheet(...) to populate it")
        return self.__balance_sheet__
