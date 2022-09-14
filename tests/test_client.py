import requests
import os


#test get available endpoints
response = requests.get('http://127.0.0.1:5000/metadata')
print(response)
print(response.json())

#test get endpoint data
response = requests.get('http://127.0.0.1:5000/api/private')
print(response)
print(response.text)

#test post authorization for private endpoint
client_id = os.environ.get("CLIENT_ID","28d5fe9684317f55d933803dfbb32992")
client_secret = os.environ.get("CLIENT_SECRET","b7b0b628d4af55431266404aa48fd131df2ffb75a0da4dac0c3f010d17d7f888")
headers = {'Content-type': 'application/json'}

response = requests.post('http://127.0.0.1:5000/api/private',
                         headers=headers,
                         auth=(client_id, client_secret))
print(response)
print(response.text)



#test get endpoint list function
'''response = requests.get('http://127.0.0.1:5000/metadata')
print(response.text)


#test create specific endpoint
response = requests.post("http://127.0.0.1:5000/api/newData",
                         json={"task1":"value1"}
                         ,auth=('test_user', 'test_password')
                         )
print(response.json())


#test append specific endpoint
response = requests.put("http://127.0.0.1:5000/api/newData"
                        ,json={"task2":"value2"}
                        ,auth=('test_user', 'test_password'))
print(response.text)



#test delete specific endpoint
response = requests.delete("http://127.0.0.1:5000/api/newData"
                           ,auth=('test_user', 'test_password')
                           )
print(response.text)



'''