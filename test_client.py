import requests
from werkzeug.security import generate_password_hash, check_password_hash

response = requests.get('http://127.0.0.1:5000/')
print(response.text)

response = requests.delete("http://127.0.0.1:5000/api/blablabla"
                           ,auth=('michiel', 'test123')
                           )
print(response)

response = requests.post("http://127.0.0.1:5000/api/newData",
                         json={"task":"test4"}
                         ,auth=('michiel', 'test123')
                         )
print(response.json())

response = requests.put("http://127.0.0.1:5000/api/filesandwhatnot"
                        ,json={"test":"hi2"}
                        ,auth=('michiel', 'test123'))
print(response)
print(response.text)

#response = requests.get("http://127.0.0.1:5000/api/tasks")
#print(response.json())
