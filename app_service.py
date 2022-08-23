import json

class AppService():

    def __init__(self):
        pass
    def get_tasks(self, instance_name):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        tasksJSON = json.dumps(data)
        return tasksJSON

    def create_task(self,instance_name,task):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        data.append(task)
        tasksJSON = json.dumps(data)
        #TODO: add save and close
        return tasksJSON

    def update_task(self, instance_name, request_task):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        for task in data:
            if task["id"] == request_task['id']:
                task.update(request_task)
                return json.dumps(data);
        # TODO: add save and close
        return json.dumps({'message': 'task id not found'});

    def delete_task(self, instance_name, request_task_id):
        open_file = open(f'instances/{instance_name}.json')
        data = json.load(open_file)
        for task in data:
            if task["id"] == request_task_id:
                data.remove(task)
                return json.dumps(data);
        # TODO: add save and close
        return json.dumps({'message': 'task id not found'});

    
