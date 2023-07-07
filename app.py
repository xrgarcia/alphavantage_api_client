import logging

from alphavantage_api_client import AlphavantageClient, CurrencyQuote
import json
from pydantic import BaseModel, Field, model_validator
from typing import Optional


# JSON data
json_reponse = {
    "Realtime Currency Exchange Rate": {
        "1. From_Currency Code": "BTC",
        "2. From_Currency Name": "Bitcoin",
        "3. To_Currency Code": "CNY",
        "4. To_Currency Name": "Chinese Yuan",
        "5. Exchange Rate": "219029.70000000",
        "6. Last Refreshed": "2023-07-07 17:15:53",
        "7. Time Zone": "UTC",
        "8. Bid Price": "219027.78000000",
        "9. Ask Price": "219035.95000000"
    }
}

# Convert JSON data to Pydantic BaseModel using model_validate_json
user = CurrencyQuote.model_validate(json_reponse)

# Print the user object
print(user)
