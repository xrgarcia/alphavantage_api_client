from abc import ABC, abstractmethod
from alphavantage_api_client import AlphavantageClient
from typing import Union

class BaseTestSuite(ABC):

    @abstractmethod
    def get_client(self) -> AlphavantageClient:
        pass

