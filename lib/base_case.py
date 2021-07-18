import json

import allure
from faker import Faker
from requests import Response


class BaseCase:
    @allure.step('Get answer')
    def get_answer(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response not have '{name}'"

        return response_as_dict[name]

    @allure.step('Get cookie')
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last Response"
        return response.cookies[cookie_name]

    @allure.step('Get header')
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last Response"
        return response.headers[headers_name]

    @allure.step('Get json value')
    def get_json_value(self, response: Response, name):
        try:
            response_as_dist = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dist, f"Response JSON doesn't have key '{name}'"

        return response_as_dist[name]

    @allure.step('Prepare test data')
    def prepare_register_data(self):
        fake = Faker()
        return {
            'username': fake.user_name(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'password': fake.password(),
            'email': fake.ascii_company_email()
        }

    @allure.step('Prepare default login data')
    def prepare_default_login_data(self):
        return {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

    @allure.step('Prepare login data')
    def prepare_login_data(self, email, password):
        return {
            'email': email,
            'password': password
        }
