import pytest
import json

from alphavantage_api_client import AlphavantageClient
from .test_all_free_endpoints import AllEndPointTests


class TestSingleClientIntegrationSuite(AllEndPointTests):

    def setup_class(cls):
        cls.__client__ = AlphavantageClient().should_retry_once().use_simple_cache(True, 10000)

    def teardown_class(cls):
        #cache = json.dumps(cls.__client__.__cache__)
        #with open("./tests/mocks/mock_data.json","w") as outfile:
        #    outfile.write(cache)
        pass

    def get_client(self) -> AlphavantageClient:
        return self.__client__

