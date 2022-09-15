# Decentralised Data Interface System V1.1

*** In Development ***

Interested in collaborating, but don't know where to start?
Visit the discussion page to suggest a feature, share your vision or ask questions about the project:
https://github.com/bureaugewas/Ddist/discussions

Want to jump right in? Features for V1.1:
https://github.com/users/bureaugewas/projects/5

How to run the app.
1. Clone the repository.
2. Set the Ddist project as environment.
3. Run the following commands in terminal:
```flask init-db```
```flask run```
4. Open the app by going to: http://127.0.0.1:5000/
5. Register a user and log in.

# Endpoint commands
1. Create an Admin token by going to 'Client_access'
2. Select 'Generate token for:' and choose 'Admin'
3. Select the amount of days you want the token to have access
4. Copy the Client_id and Client_secret to a text document

## Uploading data via endpoint

```
client_id = os.environ.get("CLIENT_ID","<Client_id>")
client_secret = os.environ.get("CLIENT_SECRET","<Client_secret>")
```

Updating data via endpoint
```
```

Deleteting data via endpoing
```
```


# User interface
Login page

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190216013-bbf25e70-1395-4126-a8ca-8fe61e70adb3.png">

Endpoint manager

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190215379-25f3b202-2780-42ad-bfa9-2027a86f6d3c.png">

Token generation

<img width="650" alt="image" src="https://user-images.githubusercontent.com/78079422/190215958-45ac1eed-7a7a-463e-a683-ad64012fe222.png">


# Future versions

v2.0
- List of other people's endpoints.
- Ability to save and query other people's endpoints and save data in the app.
- Ability to set permissions on endpoints.
- Ability to request lightning payments for data.
