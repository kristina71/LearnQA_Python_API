from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Test get user register data")
class TestUserGet(BaseCase):
    @allure.description("Test get user details not auth")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.json_has_key(response, "username")
        Assertions.json_has_no_key(response, "email")
        Assertions.json_has_no_key(response, "firstName")
        Assertions.json_has_no_key(response, "lastName")

    @allure.description("Test get user details auth as same user")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_method = self.get_answer(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.json_has_keys(response2, expected_fields)

    @allure.description("Test get data from another user")
    def test_get_data_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get(f"/user/2979",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.json_has_key(response2, "username")
        Assertions.json_has_no_key(response2, "email")
        Assertions.json_has_no_key(response2, "firstName")
        Assertions.json_has_no_key(response2, "lastName")
