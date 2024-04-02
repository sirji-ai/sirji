import os
import json

def load_config(file_name):
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct full file path
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r') as file:
        return json.load(file)