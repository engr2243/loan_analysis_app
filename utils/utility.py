import json

def load_js(file_path):
    # Open the file and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
