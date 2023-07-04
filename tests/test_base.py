from abc import ABC, abstractmethod
from alphavantage_api_client import AlphavantageClient

class BaseTestSuite(ABC):

    @abstractmethod
    def get_client(self) -> AlphavantageClient:
        pass
