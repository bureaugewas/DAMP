# Decentralized API Management Platform (DAMP) V1.1

*** In Development ***

DAMP is a Node Based Distributed Data Interfacing System. It's a node-based decentralized app (ndapp) for quickly spinning up and hosting Application Programming Interfaces (APIs). The goal is to eventually Dockerize this project and make it available on Umbrel OS and other Node Operating Systems. Use cases for this application are accountless logins-, decentralized product hosting for retail/shop platforms and decentralized social media platforms.

Interested in collaborating, but don't know where to start?
Visit the discussion page to suggest a feature, share your vision or ask questions about the project:
https://github.com/bureaugewas/DAMP/discussions

Want to jump right in? Features for V1.1:
https://github.com/users/bureaugewas/projects/5

# Running the Application
1. Clone the repository.
2. Set the DAMP project as environment.
3. Run the following commands in terminal:

```flask init-db```

```flask run```

4. Open the app by going to: http://127.0.0.1:5000/
5. Register a user and log in.


# Endpoint Commands
Endpoints can be created, updated or deleted using Post, Put and Delete methods. The following steps describe how this is done:

1. Create an Admin token by going to 'Client_access' in the user interface
2. Select 'Generate token for:' and choose 'Admin'
3. Select the amount of days you want the token to have access
4. Paste the client_id and client_secret in the following Python script

```
client_id = os.environ.get("CLIENT_ID","<Client_id>")
client_secret = os.environ.get("CLIENT_SECRET","<Client_secret>")
```


## Uploading data via POST method
5. Uploading will create a new endpoint using a POST method (Paremeter description down below):

```
headers = {'Content-type': 'application/json'}
body = {"name":"<name>",
        "status":"Active",
        "availability":"Public",
        "daily_rate_limit":200,
        "json_validation":"1",
        "data":{"test":1,"test2":2}}
```

6. Add the headers and body to the request and run the Python script:

```
response = requests.post('http://127.0.0.1:5000/api/upload',
                        headers=headers,
                        json=body,
                        auth=(client_id, client_secret))
print(response)
```

7. The newly created endpoint should now appear in the user interface


## Updating data via PUT method
5. Updating will update an existing endpoint using a PUT method:

```
headers = {'Content-type': 'application/json'}
body = {"name":"<name>",
        "status":"Active",
        "availability":"Private",
        "json_validation":0,
        "daily_rate_limit":10,
        "data": "Non Json data"}
```

6. Add the headers and body to the request and run the Python script:

```
response = requests.put('http://127.0.0.1:5000/api/update',
                        headers=headers,
                        json=body,
                        auth=(client_id, client_secret))
print(response)
```

7. The changes to the endpoint should now appear in the user interface


## Deleteting data via DELETE method
5. Deleting will delete an existing endpoint using a DELETE method:

```
headers = {'Content-type': 'application/json'}. 
body = {"name":"<name>"} OR. 
body = {"endpoint":"/api/fetch/<name>"}. 
```

6. Add the headers and body to the request and run the Python script:

```
response = requests.delete('http://127.0.0.1:5000/api/delete',  
                        headers=headers,  
                        json=body,  
                        auth=(client_id, client_secret)). 
print(response)
```

7. The endpoint should now dissapear from the user interface


### Parameter definitions
        name:                           Name of the endpoint. Will become /api/fetch/<name>.
        availability (Public/Private):  Will determine if your endpoint is publically accessible or whether a token is needed.
        status (Active/Inactive):       Will determine if your endpoint is reachable or not.
        daily_rate_limit (Integer):     Will set the daily limit an API can be called by a user (not functional yet).
        json_validation (0/1):          Will validate whether your data contains valid json.
        data:                           The data you want to make available via your endpoint. Can be plain text or json.


# User interface
Login page

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190216013-bbf25e70-1395-4126-a8ca-8fe61e70adb3.png">

Endpoint manager

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190215379-25f3b202-2780-42ad-bfa9-2027a86f6d3c.png">

Token generation

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190215958-45ac1eed-7a7a-463e-a683-ad64012fe222.png">


# Future versions
Check out ideas for future versions here:

v1.2
https://github.com/users/bureaugewas/projects/6

v2.0
https://github.com/users/bureaugewas/projects/7

Or share your ideas for features in a discussion:
https://github.com/bureaugewas/DAMP/discussions/8
