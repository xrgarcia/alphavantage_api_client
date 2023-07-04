from alphavantage_api_client import AlphavantageClient
from .test_all_free_endpoints import AllEndPointTests


class TestMultiClientIntegrationSuite(AllEndPointTests):

    def get_client(self) -> AlphavantageClient:
        return AlphavantageClient().should_retry_once()
