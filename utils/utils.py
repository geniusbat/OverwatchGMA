import yaml
import os

def load_yaml(file:str):
    if os.path.exists(file):
        with open(file, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        raise FileExistsError