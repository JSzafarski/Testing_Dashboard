import pytest
import requests
from time import time
from dotenv import load_dotenv
import os

load_dotenv()  # Automatically loads from .env in the same directory

API_KEY = os.getenv("OPEN_WEATHER_API") #load key from .env
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def weather_api_testing():
    start_time = time() #timestamp at which the test is performed
    params = {"q": "Warsaw", "appid": API_KEY} #passing a location parameter
    response = requests.get(BASE_URL, params=params)
    response_time = time() - start_time #calculaing the time to receive response

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    data = response.json()
    assert "main" in data, "response data missing the 'main' field" #ensure the structure of the response is appropriate

    return {
        "endpoint": "weather/Warsaw",
        "status": "pass" if response.status_code == 200 else "fail",
        "response_time": response_time
    }


if __name__ == "__main__":
    result = weather_api_testing()
    print(f"result: {result}")