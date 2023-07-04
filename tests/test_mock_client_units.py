from alphavantage_api_client import AlphavantageClient
from .test_all_free_endpoints import AllEndPointTests
from .mock_client import MockAlphavantageClient

class TestSingleClientUnitSuite(AllEndPointTests):

    def setup_class(cls):
        cls.__client__ = MockAlphavantageClient()

    def get_client(self) -> AlphavantageClient:
        return self.__client__
