import json

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in Response.cookies, f"Cannot find cookie with name {cookie_name} in the last Response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in Response.headers, f"Cannot find header with name {headers_name} in the last Response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dist = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dist, f"Response JSON doesn't have key '{name}'"

        return response_as_dist[name]
