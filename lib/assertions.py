import json.decoder

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_messege):
        try:
            response_as_dist = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dist, f"Response JSON doesn't have key '{name}'"
        assert response_as_dist[name] == expected_value, error_messege

    @staticmethod
    def json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"response JSON not have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response, expected_code):
        assert response.status_code == expected_code, \
            f"error! expected: {expected_code} . Actual: {response.status_code}"

    @staticmethod
    def json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"response JSON  key '{name}' is not present"

    @staticmethod
    def json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"response JSON not have key '{name}'"
