import pytest
import requests
from time import time
from dotenv import load_dotenv
import os
from requests.exceptions import RequestException # for request execption handling
load_dotenv()  # Automatically loads from .env in the same directory

API_KEY = os.getenv("OPEN_WEATHER_API") #load key from .env
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
MAX_RETRY_COUNT = 3
def make_request_with_retries(url, params):
    for attempt in range(MAX_RETRY_COUNT):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code >= 500:
                continue  # retry on server error
            return response
        except RequestException as e:
            if attempt == MAX_RETRY_COUNT - 1:
                raise RuntimeError(f"API request failed: {e}")
            return None
    return None


def weather_api_testing():
    """
    A simple function to test the weather API.
    :return: a json formatted response containing metadata related to the api test
    """
    if not API_KEY: #ensure we have an API key in our .env file
        raise ValueError("API key is missing. Please check your .env file.")
    start_time = time() #timestamp at which the test is performed
    params = {"q": "Warsaw", "appid": API_KEY} #passing a location parameter
    response = make_request_with_retries(BASE_URL, params)
    if response is None:
        print("API request failed")
        return None
    response_time = time() - start_time #calculaing the time to receive response

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    data = response.json()# convert to a json format
    assert "main" in data, "response data missing the 'main' field" #ensure the structure of the response is appropriate

    return {
        "endpoint": "weather/Warsaw",
        "status": "pass" if response.status_code == 200 else "fail",
        "response_time": response_time
    }

if __name__ == "__main__":
    result = weather_api_testing()
    print(f"result: {result}")