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

        dataJSON = new_data
        with open(f'instances/{instance_name}.json', 'w') as f:
            json.dump(dataJSON, f)
        return dataJSON

    def delete_data(self, instance_name):
        os.remove(f"instances/{instance_name}.json")
        return f"{instance_name} is removed"