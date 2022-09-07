import requests

response = requests.get('http://127.0.0.1:5000/metadata')
print(response)
print(response.json())

#test get endpoint data
response = requests.get('http://127.0.0.1:5000/api/test')
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