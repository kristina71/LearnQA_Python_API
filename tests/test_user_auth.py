import pytest
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserAuth(BaseCase):
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        url = "https://playground.learnqa.ru/api/user/login"
        response = requests.post(url, data=data)

        self.auth_sid = response.cookies.get("auth_sid")
        self.x_csrf_token = response.headers.get("x-csrf-token")
        self.user_id = response.json()["user_id"]

        self.url2 = "https://playground.learnqa.ru/api/user/auth"

    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def test_auth_user(self):
        response2 = requests.get(self.url2, headers={"x-csrf-token": self.x_csrf_token}, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id,
            "User ids should be equal"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(self.url2, headers={"x-csrf-token": self.x_csrf_token})
        else:
            response2 = requests.get(self.url2, cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )

