import os
from os import listdir
from flask import Flask, request, url_for, redirect
from app_service import AppService
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import Flask, session

#example users
users = {
    "test_user": generate_password_hash("test_password")
}

with open(f'users/users.json', 'w') as f:
    json.dump(users, f)

auth = HTTPBasicAuth()
app = Flask(__name__)
appService = AppService()

#Verify password
@auth.verify_password
def verify_password(username, password):
    open_file = open(f'users/users.json')
    auth_users = json.load(open_file)
    if username in auth_users and \
            check_password_hash(users.get(username), password):
        return username

#Human interface
@app.route('/home')
@auth.login_required
def home():
    inst_link = ''
    logout = '<br/><a href=\'/logout\'>Logout user<a></br>'
    for f in listdir('instances'):
        inst = os.path.splitext(f)[0]
        inst_link += '<a href=\'api/' + inst + '\'>' + inst + '<a></br>'

    f = open('html/upload.html','r')
    upload_template = f.read()

    return f"Hello {auth.current_user()}, Welcome to Ddist! Available instances: </br>" + inst_link + "</br>" + upload_template + logout

#Computer interface --> get endpoints
@app.route('/')
def index():
    endpoint_dict = {"endpoints":[]}
    name = ''
    for f in listdir('instances'):
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


#Upload_data
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f'instances/{f.filename}')
      url_home = '<br/><a href=\'/home\'>Return home<a></br>'
      return 'file uploaded successfully' + url_home

#logout user
@app.route('/logout')
@auth.login_required
def logout():
    #session.pop(auth.username(),None)
    url_home = '<br/><a href=\'/home\'>Return home<a></br>'
    return "Logout" + url_home, 401

if __name__ == "__main__":
    app.secret_key = 'test123'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()