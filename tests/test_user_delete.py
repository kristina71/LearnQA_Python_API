from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.story("User profile")
@allure.feature("User profile")
@allure.epic("Tests user delete")
class TestUserDelete(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Test deleting user with id 2')
    @allure.description("Test deleting user with id 2(this id users can't be deleted")
    def test_delete_user(self):
        login_data = self.prepare_default_login_data()

        user_id = 2
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        Assertions.assert_json_value_by_name(response, "user_id", user_id, "error login")

        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

        response3 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_json_value_by_name(response3, "username", "Vitaliy", "User with id=2 cannot be deleted")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Test deleting user')
    @allure.description("Test deleting user")
    def test_positive_delete_user(self):
        register_data = self.prepare_register_data()
        MyRequests.post("/user/", data=register_data)

        login_data = self.prepare_login_data(register_data['email'], register_data['password'])

        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_answer(response, "user_id")

        MyRequests.delete(f"/user/{user_id}", data=login_data,
                          headers={"x-csrf-token": token},
                          cookies={"auth_sid": auth_sid}
                          )

        response2 = MyRequests.get(f"/user/{user_id}")

        assert response2.content.decode("utf-8") == f"User not found"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Test for delete second user with having auth data in first user')
    @allure.description("Test for delete second user with having auth data in first user")
    def test_delete_another_user(self):
        login_data = self.prepare_default_login_data()

        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        self.get_answer(response, "user_id")

        response2 = MyRequests.delete(f"/user/4087", data=login_data,
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        assert response2.content.decode("utf-8") != f"User not found"
