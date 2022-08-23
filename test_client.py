import requests

response = requests.get('http://127.0.0.1:5000/')
print(response.text)

response = requests.post("http://127.0.0.1:5000/api/blablabla", json={"task":"test4"})
print(response.json())

# Update an existing resource
#requests.put('https://httpbin.org/put', data = {'key':'value'})

response = requests.get("http://127.0.0.1:5000/api/tasks")
print(response.json())

response = requests.delete("http://127.0.0.1:5000/api/images")
print(response)