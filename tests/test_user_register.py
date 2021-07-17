import allure
from faker import Faker

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Tests for user registrations")
class TestUserRegister(BaseCase):
    @allure.description("Test create user successfully")
    def test_create_user_successfully(self):
        fake = Faker()

        data = {
            'username': fake.user_name(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': fake.ascii_company_email()
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.json_has_key(response, "id")

    @allure.description("Test create user with existing email")
    def test_create_user_with_existing_email(self):
        fake = Faker()

        email = 'vinkotov@example.com'
        data = {
            'username': fake.user_name(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': email
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"actual content {response.status_code}"

    @allure.description("Test create user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        fake = Faker()

        email = 'vinkotovexample.com'
        data = {
            'username': fake.user_name(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': email
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @allure.description("Test create user with short username")
    def test_create_user_with_short_username(self):
        fake = Faker()

        data = {
            'username': fake.pystr(min_chars=None, max_chars=1),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': fake.ascii_company_email()
        }
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    @allure.description("Test create user with long username")
    def test_create_user_with_long_username(self):
        fake = Faker()

        data = {
            'username': fake.pystr(min_chars=None, max_chars=260),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': fake.ascii_company_email()
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long"

    exclude_params = [
        'username',
        'firstName',
        'lastName',
        'password',
        'email'
    ]

    @allure.description("Test create user with not one parameter")
    @pytest.mark.parametrize('exclude_params', exclude_params)
    def test_create_user_with_not_one_parameter(self, exclude_params):
        fake = Faker()

        data = {
            'username': fake.user_name(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': fake.ascii_company_email()
        }

        data.pop(exclude_params)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_params}"
