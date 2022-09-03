import os
import json

from app import app
from os import listdir
from flask import Flask, request, url_for, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session
from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        # Skip if username/password not set
        ddist_user = os.getenv('DDIST_USER', '')
        ddist_pass = os.getenv('DDIST_PASS', '')
        if (not ddist_user or not ddist_pass) or (
                auth
                and ddist_user == auth.username
                and ddist_pass == auth.password):
            return f(*args, **kwargs)
        else:
            return make_response('Not logged in', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

'''#Verify password
@auth.verify_password
def verify_password(username, password):
    open_file = open(f'../config/users.json')
    auth_users = json.load(open_file)
    if username in auth_users and \
            check_password_hash(users.get(username), password):
        return username'''

#Human interface
@app.route('/')
@auth_required
def home():
    inst_link = ''
    logout = '<br/><a href=\'/auth/logout\'>Logout user<a></br>'
    for f in listdir('instances'):
        inst = os.path.splitext(f)[0]
        inst_link += '<a href=\'api/' + inst + '\'>' + inst + '<a></br>'

    f = open(app.config['UPLOAD_PATH'], 'r')
    upload_template = f.read()

    return f"Hello, Welcome to Ddist! Available instances: </br>" + inst_link + "</br>" + upload_template + logout

#Computer interface --> get endpoints
@app.route('/meta')
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
    open_file = open(f'instances/{instance_name}.json')
    data = json.load(open_file)
    dataJSON = json.dumps(data)
    return dataJSON

#create new data
@app.route('/api/<instance_name>', methods=['POST'])
@auth_required
def create_data(instance_name):
    if not request.json:
        abort(400)
    request_json = request.get_json()
    with open(f'instances/{instance_name}.json', 'w') as f:
        json.dump(request_json, f)
    return request_json

#delete data
@app.route(f'/api/<instance_name>', methods=['DELETE'])
@auth_required
def delete_data(instance_name):
    os.remove(f"instances/{instance_name}.json")
    return f"{instance_name} is removed"

#Append data
@app.route('/api/<instance_name>', methods=['PUT'])
@auth_required
def append_data(instance_name):
    request_json = request.get_json()
    open_file = open(f'instances/{instance_name}.json')
    data = json.load(open_file)
    for k in request_json.keys():
        data[k] = request_json[k]
    with open(f'instances/{instance_name}.json', 'w') as f:
        json.dump(data, f)
    return data

#Upload_data
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f'instances/{f.filename}')
      url_home = '<br/><a href=\'/\'>Return home<a></br>'
      return 'file uploaded successfully' + url_home

#logout user
@app.route('/logout')
@auth_required
def logout():
    #session.pop(auth.username(),None)
    url_home = '<br/><a href=\'/\'>Return home<a></br>'
    return "Logout" + url_home, 401

if __name__ == "__main__":
    app.secret_key = 'test123'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run('0.0.0.0', 5000, debug=True)