import pytest

from alphavantage_api_client import AlphavantageClient
from .test_all_endpoints import AllEndPointTests


class TestSingleClientIntegrationSuite(AllEndPointTests):

    def setup_class(cls):
        cls.__client__ = AlphavantageClient().should_retry_once()

    def get_client(self) -> AlphavantageClient:
        return self.__client__
