import pytest
import requests
import json

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        assert "HomeWork" in response.cookies, "There is no HomeWork cookie in the response"
        print(response.cookies.get_dict()["HomeWork"])
        assert "hw_value" in response.cookies.get_dict()["HomeWork"], "There is no hw_value value in the cookie"

