import requests

print('Hello from Kris')

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
