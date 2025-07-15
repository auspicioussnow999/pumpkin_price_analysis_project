import os
import json

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)