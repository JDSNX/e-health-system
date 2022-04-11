import json
import time
import requests

from requests.structures import CaseInsensitiveDict
from flask import Flask, request, render_template

application = Flask(__name__)

url = "https://ae-keys-1f1e9-default-rtdb.asia-southeast1.firebasedatabase.app/"
headers = CaseInsensitiveDict
headers = {"Content-Type": "application.json"}

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@application.route('/get', methods=['GET'])
def get_all():
    try:
        resp = requests.get(url=f"{url}/users.json", headers=headers)

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.json(), "timestamp": time.time()}

@application.route('/get_user', methods=['GET'])
def get_user(ref_id=None):
    try:
        ref_id = str(request.args['ref_id'])

        resp = requests.get(url=f"{url}/users/{ref_id}.json", headers=headers)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.json(), "timestamp": time.time()}

@application.route('/update_pass', methods=['GET'])
def update_pass():
    try:
        ref_id = str(request.args['ref_id'])
        password = str(request.args['password'])

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "timestamp": time.time()}

        data = {"password": password, "timestamp": time.time()}
        data = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@application.route('/delete', methods=['GET'])
def delete_user():
    try:
        ref_id = str(request.args['ref_id'])

        resp = requests.delete(url=f"{url}/users/{ref_id}.json", headers=headers)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}
