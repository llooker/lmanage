import json
from ruamel.yaml import YAML
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class Yaml:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        yaml = YAML()
        with open(self.yaml_path, 'r') as file:
            self.parsed_yaml = yaml.load(file)

    def get_permission_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            x = type(objects)
            t = list(objects.keys())
            if 'permissions' in list(objects.keys()):
                response.append(objects)
        response = [r for r in response if r.get('name') != 'Admin']
        return response

    def get_model_set_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'models' in list(objects.keys()):
                response.append(objects)
        return response

    def get_role_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'permission_set' and 'model_set' in list(objects.keys()):
                response.append(objects)
        response = [r for r in response if r.get('name') != 'Admin']
        return response

    def get_folder_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            print(objects)
            if 'content_metadata_id' in list(objects.__dict__.keys()):
                response.append(objects)
        return response

    def get_user_attribute_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'hidden_value' in list(objects.keys()):
                response.append(objects)
        return response

    def get_look_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'query_obj' in list(objects.keys()):
                response.append(objects)
        return response
    
    def get_dash_metadata(self):
        response = []
        for objects in self.parsed_yaml:
            if 'lookml' in list(objects.keys()):
                response.append(objects)
        return response
