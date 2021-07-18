import json.decoder

import allure
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        with allure.step(f"Assert JSON value by name {name}"):
            try:
                response_as_dist = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not in JSON format. Response text is '{response.text}'"

            assert name in response_as_dist, f"Response JSON doesn't have key '{name}'"
            assert response_as_dist[name] == expected_value, error_message

    @staticmethod
    def json_has_key(response: Response, name):
        with allure.step(f"Assert JSON value by key {name}"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response text is '{response.text}'"

            assert name in response_as_dict, f"response JSON not have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response, expected_code):
        with allure.step(f"Assert code status {expected_code}"):
            assert response.status_code == expected_code, \
                f"error! expected: {expected_code} . Actual: {response.status_code}"

    @staticmethod
    def json_has_no_key(response: Response, name):
        with allure.step(f"Assert JSON has no key {name}"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response text is '{response.text}'"

            assert name not in response_as_dict, f"response JSON  key '{name}' is not present"

    @staticmethod
    def json_has_keys(response: Response, names: list):
        with allure.step(f"Assert JSON has keys {names}"):
            try:
                response_as_dict = response.json()
            except json.JSONDecodeError:
                assert False, f"Response is not JSON format. Response text is '{response.text}'"

            for name in names:
                assert name in response_as_dict, f"response JSON not have key '{name}'"

