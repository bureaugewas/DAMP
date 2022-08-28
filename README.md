# Decentralised Data Interface System
Or Ddist for short

Ddist is a Docker based Umbrel application for quickly spinning up and hosting Application Computer Interfaces (or APIs).
This project is very much in progress and not for profit. Help is greatly appreciated.


V1.0 (In progress) The goal of the first implementation is to build a simple Docker based API with basic data interfacing functionalities:

- Ability to create one or multiple API instances with named endpoint. (DONE)
- Ability to upload a .json file to that instance that can be directly queried over the internet. (DONE)
- Ability for the owner of an endpoint instance to POST, PUT or DELETE .json data. (DONE)
- Simple User interface for login, logout and uploading files. (DONE)
- File upload from interface. (DONE)
- Docker application that can be run on Umbrel.

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
