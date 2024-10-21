import os
import yaml

def getYamlConfig():
    file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)