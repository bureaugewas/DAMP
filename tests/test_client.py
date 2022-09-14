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
client_id = os.environ.get("CLIENT_ID","faf03b6b7941c4090c1cd4673efbcfe8")
client_secret = os.environ.get("CLIENT_SECRET","8bf7803759f83b0d6b2eb6f3028a2bd30a3d08cdd95ec64da47e2c64ef970912")
headers = {'Content-type': 'application/json'}

response = requests.get('http://127.0.0.1:5000/api/fetch/nieuwe_data',
                         headers=headers,
                         auth=(client_id, client_secret))
print(response)
print(response.text)

#test create endpoint
client_id = os.environ.get("CLIENT_ID","126c81b234db2cdf57fed5b6f6958724")
client_secret = os.environ.get("CLIENT_SECRET","07701727617299a47ba587e94e7eeeb76d0cfcbc4193962a0b6e46779fc02070")
headers = {'Content-type': 'application/json'}
body = {"name":"data11312",
        "status":"Inactive",
        "availability":"Private",
        "data":{"test":12,
                "test2":12}}

response = requests.post('http://127.0.0.1:5000/api/upload',
                        headers=headers,
                        json=body,
                        auth=(client_id, client_secret))
print(response)
print(response.text)

#test update endpoint
client_id = os.environ.get("CLIENT_ID","126c81b234db2cdf57fed5b6f6958724")
client_secret = os.environ.get("CLIENT_SECRET","07701727617299a47ba587e94e7eeeb76d0cfcbc4193962a0b6e46779fc02070")
headers = {'Content-type': 'application/json'}
body = {"name":"data11312",
        "availability": "Public",
        "status": "Active",
        "json_validation":0,
        "daily_rate_limit":10,
        "data": "hallo"}

response = requests.put('http://127.0.0.1:5000/api/update',
                        headers=headers,
                        json=body,
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