import os
from os import listdir
from flask import Flask, request, url_for
from app_service import AppService
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("hello"),
    "michiel": generate_password_hash("test123")
}

with open(f'users/users.json', 'w') as f:
    json.dump(users, f)

auth = HTTPBasicAuth()
app = Flask(__name__)
instances = listdir('instances')
appService=AppService()

@auth.verify_password
def verify_password(username, password):
    open_file = open(f'users/users.json')
    auth_users = json.load(open_file)
    if username in auth_users and \
            check_password_hash(users.get(username), password):
        return username

#Human interface
@app.route('/index')
@auth.login_required
def home():
    inst_link = ''
    for f in instances:
        inst = os.path.splitext(f)[0]
        inst_link += '<a href=\'api/' + inst + '\'>' + inst + '<a></br>'
    return f"Hello {auth.current_user()}, Welcome to Ddist! Available instances: </br>" + inst_link

#Computer interface --> get endpoints
@app.route('/')
def index():
    endpoint_dict = {"endpoints":[]}
    name = ''
    for f in instances:
        endpoint = {}
        name = os.path.splitext(f)[0]
        endpoint[name] = 'api/' + name
        endpoint_dict["endpoints"].append(endpoint)
    return endpoint_dict

#get data
@app.route('/api/<instance_name>')
def get_data(instance_name):
    return appService.get_data(instance_name)

#create new data
@app.route('/api/<instance_name>', methods=['POST'])
@auth.login_required
def create_data(instance_name):
    if not request.json:
        abort(400)
    request_json = request.get_json()
    return appService.create_data(instance_name,request_json)

#delete data
@app.route(f'/api/<instance_name>', methods=['DELETE'])
@auth.login_required
def delete_data(instance_name):
    return appService.delete_data(instance_name)

#Append data
@app.route('/api/<instance_name>', methods=['PUT'])
@auth.login_required
def append_data(instance_name):
    request_json = request.get_json()
    return appService.append_data(instance_name,request_json)