from alphavantage_api_client import Ticker
import pytest
import logging
import json


@pytest.mark.integration
def test_fiscal_date_ending_field_in_all_accounting_reports():
    vz = Ticker().create_client().should_retry_once().from_symbol("VZ").fetch_accounting_reports()
    earnings = vz.get_earnings()
    income_statement = vz.get_income_statement()
    balance_sheet = vz.get_balance_sheet()

    for index, account_report in enumerate(earnings.annualReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    for index, account_report in enumerate(earnings.quarterlyReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    for index, account_report in enumerate(income_statement.quarterlyReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    for index, account_report in enumerate(income_statement.quarterlyReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    for index, account_report in enumerate(balance_sheet.quarterlyReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    for index, account_report in enumerate(balance_sheet.quarterlyReports):
        assert "fiscalDateEnding" in account_report, f"Did not find fiscalDateEnding in {account_report}"

    logging.warning("Found fiscalDateEnding in all accounting reports")