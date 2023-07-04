import time

import requests
import os
import configparser
from alphavantage_api_client import ValidationRuleChecks, AlphavantageClient
import json
import copy
import logging


class MockAlphavantageClient(AlphavantageClient):

    def __init__(self):
        super().__init__()
        path = os.getcwd()
        logging.info(f"current path = {path}")
        self.base_path = f"{path}/tests/mocks"
        if not os.path.exists(self.base_path):
            logging.info(f"I must be running from pycharm as a test since cwd is {self.base_path}, need to fix")
            path = os.path.dirname(os.getcwd())
            os.chdir(path) # go up a directory
            path = os.getcwd()
            self.base_path = f"{path}/tests/mocks"

        logging.info(f"self.base_path = {self.base_path}")
        self.load_cache_from_disk()

    def load_cache_from_disk(self):
        self.use_simple_cache()
        with open(f"{self.base_path}/mock_data.json",'r') as file:
            json_string = file.read()
        cache = json.loads(json_string)
        self.__cache__ = cache

    def get_data_from_alpha_vantage(self, event: dict, should_retry: bool = False) -> dict:
        """
        This is the underlying function that talks to alphavantage api.  Feel free to pass in any parameters supported
        by the api.  You will receive a dictionary with the response from the web api. In addition, you will obtain
        the ``success``, ``error_message`` and ``limit_reached`` fields.
        Args:
            event (dictionary): The url parameters supported by the web api

        Returns:
            :rtype: dict

        """
        # validate api key and insert into the request if needed
        checks = ValidationRuleChecks().from_customer_request(event)
        self.__validate_api_key__(checks, event)

        # create a version of the event without api key
        loggable_event = copy.deepcopy(event)
        loggable_event.pop("apikey")

        # check cache if allowed
        if self.__use_cache__:
            results = self.__get_item_from_cache__(loggable_event)
            logging.info(f"Found item in cache: {results}")
            if results is not None:
                logging.info(json.dumps({"method": "mock.get_data_from_alpha_vantage"
                                            , "action": "return_value", "data": results,
                                         "event": loggable_event}))
                return results
        json_response = dict()
        json_response["success"] = False
        json_response["limit_reached"] = False
        json_response["status_code"] = 200
        if "symbol" in event:
            json_response["symbol"] = event["symbol"]
        json_response["error_message"] = "Could not find requested data"
        return json_response
