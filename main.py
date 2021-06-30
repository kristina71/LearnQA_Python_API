import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"


def get_status(auth_token, expected_status, flag):
    response_text = requests.get(url, params={"token": auth_token})
    json_text = json.loads(response_text.text)
    print(json_text)
    print(flag)

    if flag:
        try:
            print(json_text["result"])
        except Exception:
            print('Cannot find a result')
            exit()

    try:
        if json_text["status"] != expected_status:
            print("Incorrect status. Status code should be '" + expected_status + "'")
            print(json_text["status"])
            exit()
    except Exception:
        print('Cannot find a status value')
    return json_text["status"]


response = requests.get(url)
if response.status_code == 200:
    response_json_text = json.loads(response.text)
    try:
        token = response_json_text["token"]

        try:
            seconds = response_json_text["seconds"]

            print(get_status(token, "Job is NOT ready", 0))

            time.sleep(seconds)

            print(get_status(token, "Job is ready", 1))

        except Exception:
            print('Cannot find a seconds value')

    except Exception:
        print('Cannot find a token value')

else:
    print("Something went wrong")
