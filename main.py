import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# Wrong method provided
response_without_params = requests.get(url)
print(response_without_params.text)

# {"success":"!"}
response_with_params = requests.get(url, params={"method": "GET"})
print(response_with_params.text)

# Wrong method provided
response_with_incorrect_params = requests.get(url, params={"method": "HEAD"})
print(response_with_incorrect_params.text)

methods = ["GET", "POST", "PUT", "DELETE"]
print(methods)

for method in methods:
    if method == "GET":
        response = requests.get(url, params={"method": method})
        print("method="+method+" "+response.text)
        response = requests.post(url, params={"method": method})
        print("method="+method+" "+response.text)
        response = requests.put(url, params={"method": method})
        print("method="+method+" "+response.text)
        response = requests.delete(url, params={"method": method})
        print("method="+method+" "+response.text)
    else:
        response = requests.get(url, data={"method": method})
        print("method="+method+" "+response.text)
        response = requests.post(url, data={"method": method})
        print("method="+method+" "+response.text)
        response = requests.put(url, data={"method": method})
        print("method="+method+" "+response.text)
        response = requests.delete(url, data={"method": method})
        print("method="+method+" "+response.text)
