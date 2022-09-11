import requests
import os

#test get available endpoints
response = requests.get('http://127.0.0.1:5000/metadata')
print(response)
print(response.json())

#test get endpoint data
response = requests.get('http://127.0.0.1:5000/api/fietshuiswerk')
print(response)
print(response.text)

#test post authorization for private endpoint
client_id = os.environ.get("CLIENT_ID","7e40577d91897d6b836cebd08129a4f6")
client_secret = os.environ.get("CLIENT_SECRET","bd39e4dd67df0f6e5817f105e369743efcbf0da45a86d60a8805ce432c30fffa")
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