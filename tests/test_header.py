import pytest
import requests

from lib.base_case import BaseCase


class TestHeader(BaseCase):
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        assert "x-secret-homework-header" in response.headers, "There is no secret homework header in the response"
        print(response.headers["x-secret-homework-header"])
        assert "Some secret value" in response.headers["x-secret-homework-header"], "There is no some " \
                                                                                    "secret value in the " \
                                                                                    "header "
