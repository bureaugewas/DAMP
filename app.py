from os import listdir
import os
from os.path import isfile, join
from flask import Flask, request, url_for
from app_service import AppService
import json

app = Flask(__name__)
instances = listdir('instances')
endpoint_dict = {}

@app.route('/')
def home():
    inst_link = ''
    for f in instances:
        inst = os.path.splitext(f)[0]
        inst_link += '<a href=\'api/' + inst + '\'>' + inst + '<a></br>'

    return "Welcome to Ddist! Available instances: </br>" + inst_link

appService=AppService()

@app.route('/api/<instance_name>')
def tasks(instance_name):
    return appService.get_tasks(instance_name)

@app.route(f'/api/<instance_name>', methods=['POST'])
def create_task(instance_name):
    request_data = request.get_json()
    task = request_data['task']
    return appService.create_task(instance_name,task)

@app.route(f'/api/<instance_name>', methods=['PUT'])
def update_task(instance_name):
    request_data = request.get_json()
    return appService.update_task(instance_name,request_data['task'])

@app.route(f'/api/<instance_name>/<int:id>', methods=['DELETE'])
def delete_task(instance_name,id):
    return appService.delete_task(instance_name,id)


#for i in instances:

  #  endpoint_dict[i] = AppEndpoint(i)

