# user.py

import json
import os

cwd = os.path.abspath(os.getcwd())
cred = os.path.join(cwd, 'credentials.json')

def register(username, password):
    if not os.path.isfile(cred):
        with open(cred, 'w') as file:
            pass

    with open(cred, 'r') as file:
        data = file.read()
        if not data:
            data = {}
            data['username'] = [username]
            data['password'] = [password]
        else:
            data = json.loads(data)
            if username in data['username']:
                return False
            data['username'].append(username)
            data['password'].append(password)
    with open(cred, 'w') as file:
        json.dump(data, file)
    return True

def login(username, password):
    if not os.path.isfile(cred):
        with open(cred, 'w') as file:
            pass
        
    with open(cred, 'r') as file:
        data = file.read()
        if not data:
            return False
        data = json.loads(data)
        try:
            index = data['username'].index(username)
            if data['password'][index] == password:
                return True
            return False
        except ValueError:
            return False

