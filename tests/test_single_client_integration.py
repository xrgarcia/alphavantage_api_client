import pytest
import json

from alphavantage_api_client import AlphavantageClient
from .test_all_free_endpoints import AllEndPointTests


class TestSingleClientIntegrationSuite(AllEndPointTests):

    def setup_class(cls):
        cls.__client__ = AlphavantageClient().should_retry_once().use_simple_cache()

    def get_client(self) -> AlphavantageClient:
        return self.__client__

