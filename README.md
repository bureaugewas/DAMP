# Decentralised Data Interface System

Ddist is a Docker based Umbrel application for quickly spinning up and hosting Application Computer Interfaces (or APIs).
This project is very much in progress and not for profit. Help is greatly appreciated.


V1.0 Features:

- Create one or multiple API instances with named endpoint.
- Upload a .json file to that instance that can be directly queried over the internet.
- Ability for the owner of an endpoint instance to POST, PUT or DELETE .json data.
- Simple User interface for login, logout and uploading files.
- File upload from interface.

How to use Ddist:
1. Install Docker
2. Open the project in Pycharm
3. Build the Docker Image (e.g. from your Pycharm terminal):
```
docker build -t ddist-api .
```
4. Run the docker application
```
docker run -d -p 5000:5000 --name python-restapi ddist-api
```
5. Visit: http://127.0.0.1:5000/
6. Login with the test user
```
test_user:test_password
```
6. Create an new API endpoint by either uploading a .json file or using any of the following commands:
```
response = requests.post("http://127.0.0.1:5000/api/<endpoint_name>",
                         json={"key1":"value1"}
                         ,auth=('test_user', 'test_password')
                         )
```
7. Other ways to interact with the API: 
```
# Get endpoint list
requests.get('http://127.0.0.1:5000/meta')

# Query endpoint
requests.get('http://127.0.0.1:5000/api/<endpoint_name>')

# Append new data
requests.put("http://127.0.0.1:5000/api/<endpoint_name>"
                        ,json={"key2":"value2"}
                        ,auth=('test_user', 'test_password'))
# Delete endpoint
requests.delete("http://127.0.0.1:5000/api/<endpoint_name>"
                      ,auth=('test_user', 'test_password')
                      )
```

Future versions:

V1.1
- Secure login and token generation
- Ability to query a nodes available endpoints including some metadata.
- Ability to activate and deactive API instances.
- Ability to set API rate limits.
- Security features

v2.0
- List of other people's endpoints.
- Ability to save and query other people's endpoints and save data in the app.
- Ability to set permissions on endpoints.
- Ability to request lightning payments for data.
