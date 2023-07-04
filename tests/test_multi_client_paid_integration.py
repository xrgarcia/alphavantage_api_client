from alphavantage_api_client import AlphavantageClient
from .test_all_paid_endpoints import AllPaidEndPointTests


class TestMultiClientPaidIntegrationSuite(AllPaidEndPointTests):

    def get_client(self) -> AlphavantageClient:
        return AlphavantageClient().should_retry_once()