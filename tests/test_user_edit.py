from faker import Faker
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Tests for edit user")
class TestUserEdit(BaseCase):
    @allure.description("Test for success create user")
    def test_edit_just_created_user(self):
        register_data = self.prepare_register_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.json_has_key(response, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_answer(response, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        fake = Faker()
        new_name = fake.first_name()

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name"
        )

    @allure.description("Test for edit data user not have auth")
    def test_try_edit_user_not_auth(self):
        fake = Faker()
        new_name = fake.first_name()

        response = MyRequests.put(
            f"/user/3619",
            data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Auth token not supplied"

    @allure.description("Test for edit data first user, have auth second user")
    def test_try_edit_another_user(self):
        register_data = self.prepare_register_data()
        response = MyRequests.post("/user/", data=register_data)

        first_name = register_data['firstName']
        user_id = self.get_answer(response, "id")

        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        register_data1 = self.prepare_register_data()
        MyRequests.post("/user/", data=register_data1)

        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }

        response2 = MyRequests.post("/user/login", data=login_data1)
        auth_sid2 = self.get_cookie(response2, "auth_sid")
        token2 = self.get_header(response2, "x-csrf-token")

        fake = Faker()
        new_name = fake.first_name()

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
            data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Wrong name"
        )

    @allure.description("Test for change email without symbol @")
    def test_change_email_with_incorrect_data(self):
        register_data = self.prepare_register_data()
        response = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_answer(response, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        new_email = "cgdfgdfg.ru"

        MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email})

        response2 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "email",
            f'{email}',
            "Wrong email"
        )

    @allure.description("Test for changing firstName with min len")
    def test_change_firstname_min_len(self):
        register_data = self.prepare_register_data()
        response = MyRequests.post("/user/", data=register_data)

        first_name = register_data['firstName']
        user_id = self.get_answer(response, "id")

        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        fake = Faker()
        new_name = fake.pystr(min_chars=None, max_chars=1)

        MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        response2 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            f'{first_name}',
            "Wrong name"
        )
