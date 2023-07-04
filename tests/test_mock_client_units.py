from alphavantage_api_client import AlphavantageClient
from .test_all_endpoints import AllEndPointTests
from .mock_client import MockAlphavantageClient

class TestMultiClientUnitSuite(AllEndPointTests):

    def get_client(self) -> AlphavantageClient:
        return MockAlphavantageClient()
