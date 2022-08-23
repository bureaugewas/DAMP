import os
from os import listdir
from flask import Flask, request, url_for
from app_service import AppService

app = Flask(__name__)
instances = listdir('instances')
appService=AppService()

#Human interface
@app.route('/home')
def home():
    inst_link = ''
    for f in instances:
        inst = os.path.splitext(f)[0]
        inst_link += '<a href=\'api/' + inst + '\'>' + inst + '<a></br>'
    return "Welcome to Ddist! Available instances: </br>" + inst_link

#Computer interface
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
def create_data(instance_name):
    new_data = request.get_json()
    return appService.create_data(instance_name,new_data)

#delete data
@app.route(f'/api/<instance_name>', methods=['DELETE'])
def delete_data(instance_name):
    return appService.delete_data(instance_name)

#TODO: Append data

#TODO: Update data

