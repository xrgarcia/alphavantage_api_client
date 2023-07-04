from alphavantage_api_client import AlphavantageClient
from .test_core import CoreApiEndPointTests


class TestMultiClientIntegrationSuite(CoreApiEndPointTests):

    def get_client(self) -> AlphavantageClient:
        return AlphavantageClient().should_retry_once()
