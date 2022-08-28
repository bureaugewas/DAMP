import requests

#test get endpoint list function
response = requests.get('http://127.0.0.1:5000/')
print('Get endpoint list:')
print(response.text)

#test create specific endpoint
response = requests.post("http://127.0.0.1:5000/api/newData",
                         json={"task1":"value1"}
                         ,auth=('test_user', 'test_password')
                         )
print('Create specific endpoint:')
print(response.json())

#test get endpoint list function
response = requests.get('http://127.0.0.1:5000/')
print('Get endpoint list:')
print(response.text)

#test append specific endpoint
response = requests.put("http://127.0.0.1:5000/api/newData"
                        ,json={"task2":"value2"}
                        ,auth=('test_user', 'test_password'))
print('Append to endpoint:')
print(response.text)

#test delete specific endpoint
response = requests.delete("http://127.0.0.1:5000/api/newData"
                           ,auth=('test_user', 'test_password')
                           )
print('Delete specific endpoint:')
print(response)

#test get endpoint list function
response = requests.get('http://127.0.0.1:5000/')
print('Get endpoint list:')
print(response.text)