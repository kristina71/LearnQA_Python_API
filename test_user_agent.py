import pytest
import requests
import json


class TestUserAgent:
    data = [
        (
            {
                "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) "
                              "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                "expected_platform": "Mobile",
                "expected_browser": "No",
                "expected_device": "Android"
            }
        ),
        (
            {
                "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                              "CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
                "expected_platform": "Mobile",
                "expected_browser": "Chrome",
                "expected_device": "iOS"
            }
        ),
        (
            {
                "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "expected_platform": "Googlebot",
                "expected_browser": "Unknown",
                "expected_device": "Unknown"
            }
        ),
        (
            {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
                "expected_platform": "Web",
                "expected_browser": "Chrome",
                "expected_device": "No"
            }
        ),
        (
            {
                "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                              "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                "expected_platform": "Mobile",
                "expected_browser": "No",
                "expected_device": "iPhone"
            }
        ),
    ]

    @pytest.mark.parametrize('data', data)
    def test_user_agent(self, data):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        response = requests.get(url, headers={"User-Agent": data["user_agent"]})
        json_text = json.loads(response.text)

        assert "user_agent" in json_text, "There is no user agent in the response"
        assert json_text["user_agent"] == data[
            "user_agent"], f"Expected user agent is {data['user_agent']}, actual is {json_text['user_agent']}"

        assert "platform" in json_text, "There is no platform in the response"
        assert json_text["platform"] == data[
            "expected_platform"], f"Expected platform is {data['expected_platform']}, actual is {json_text['platform']}"

        assert "browser" in json_text, "There is no browser in the response"
        assert json_text["browser"] == data[
            "expected_browser"], f"Expected browser is {data['expected_browser']}, actual is {json_text['browser']}"

        assert "device" in json_text, "There is no device in the response"
        assert json_text["device"] == data[
            "expected_device"], f"Expected device is {data['expected_device']}, actual is {json_text['device']}"
