import json
from flask import Flask, request

import firebase
import time

application = Flask(__name__)

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@application.route('/', methods=['GET'])
def index():
    return {"success": True, "timestamp": time.time()}

@application.route('/get', methods=['GET'])
def get_all():
    try:
        fb = firebase.Firebase("", "").get_all()
        
    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": fb, "timestamp": time.time()}


@application.route('/get_user', methods=['GET'])
def get_user():
    try:
        ref_id = str(request.args['ref_id'])
        fb = firebase.Firebase(ref_id, "").get_user()

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": fb, "timestamp": time.time()}