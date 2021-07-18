import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.story("User profile")
@allure.feature("User profile")
@allure.epic("Tests user auth")
class TestUserAuth(BaseCase):
    def setup(self):
        data = self.prepare_default_login_data()

        response = MyRequests.post("/api/user/login", data=data)

        self.auth_sid = response.cookies.get("auth_sid")
        self.x_csrf_token = response.headers.get("x-csrf-token")
        self.user_id = response.json()["user_id"]

    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Test auth user')
    @allure.description("Test auth user")
    def test_auth_user(self):
        response2 = MyRequests.get("/api/user/auth", headers={"x-csrf-token": self.x_csrf_token},
                                   cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id,
            "User ids should be equal"
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Test negative auth user')
    @allure.description("Test negative auth user")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response = MyRequests.get("/api/user/auth", headers={"x-csrf-token": self.x_csrf_token})
        else:
            response = MyRequests.get("/api/user/auth", cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
