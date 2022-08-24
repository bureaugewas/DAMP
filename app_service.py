import json
import os

class AppService():

    def __init__(self):
        pass

    def get_data(self, instance_name):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        dataJSON = json.dumps(data)
        return dataJSON

    def create_data(self,instance_name,new_data):
        with open(f'instances/{instance_name}.json', 'w') as f:
            json.dump(new_data, f)
        return new_data

    def delete_data(self, instance_name):
        os.remove(f"instances/{instance_name}.json")
        return f"{instance_name} is removed"

    def append_data(self, instance_name, new_data):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        for k in new_data.keys():
            data[k] = new_data[k]
        with open(f'instances/{instance_name}.json', 'w') as f:
            json.dump(data, f)
        return data

#TODO: add update data
    def update_data(self, instance_name, request_task):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        for task in data:
            if task["id"] == request_task['id']:
                task.update(request_task)
                return json.dumps(data);
        # TODO: add save and close
        return json.dumps({'message': 'task id not found'})