import json
import time
import requests
import uuid
import os

from requests.structures import CaseInsensitiveDict
from flask import Flask, request, render_template
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

class EHS():
    load_dotenv()

    def __init__(self):        
        self.URL = os.getenv('DB_URL')
        self.SMS_API_KEY = os.getenv('SMS_API_KEY')
        self.SMS_URL = os.getenv('SMS_URL')
        self.headers = CaseInsensitiveDict
        self.headers = {"Content-Type": "application.json"}
        
    def generator(self):
        return uuid.uuid4().hex.upper()[0:5]

    def check_user(self, ref_id=None):
        try:
            resp = requests.get(url=f"{self.URL}/users/{ref_id}.json", headers=self.headers)

            if resp.json() is None:
                return {"success": False, "timestamp": time.time()}

        except Exception as e:
            return {"success": False, "msg": e, "timestamp": time.time()}

        return {"success": True, "result": resp.json(), "timestamp": time.time()}

class ModuleResult(BaseModel):
    BLOOD_OXYGEN_LEVEL: str
    BODY_TEMPERATURE: str
    ECG_RESULT: str

class Data(BaseModel):
    ref_id: Optional[str] = None
    first_name: str
    last_name: str
    middle_initial: Optional[str] = None
    emergency_contact_person: str
    emergency_contact_number: str
    result: Optional[ModuleResult] = None
    timestamp: Optional[str] = time.time()
    password: Optional[str] = None

app = Flask(__name__)
ehs = EHS()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get', methods=['GET'])
def get_all():
    if request.method == 'POST':
        return "Nuh-uh!"

    if request.method == 'GET':
        try:
            resp = requests.get(url=f"{ehs.URL}/users.json", headers=ehs.headers)

        except Exception as e:
            return {"success": False, "msg": e, "timestamp": time.time()}

        return {"success": True, "result": resp.json(), "timestamp": time.time()}

@app.route('/get_user', methods=['GET'])
def get_user(ref_id=None):
    try:
        ref_id = str(request.args['ref_id'])
        resp = requests.get(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.json(), "timestamp": time.time()}

@app.route('/update_pass', methods=['POST'])
def update_pass():
    try:
        data_json = request.get_json()
        ref_id = data_json['ref_id']
        password = data_json['password']

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "msg": "User not found!", "timestamp": time.time()}

        data = {"password": password, "timestamp": time.time()}
        data = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/delete', methods=['GET'])
def delete_user():
    try:
        ref_id = str(request.args['ref_id'])

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "msg": "User not found!", "timestamp": time.time()}

        resp = requests.delete(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers)

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        data_json = request.get_json()
        ref_id = data_json['ref_id']

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "msg": "User not found!", "timestamp": time.time()}
        
        data = Data(
            ref_id=ref_id,
            first_name=data_json['first_name'],
            last_name=data_json['last_name'],
            middle_initial=data_json['middle_initial'],
            emergency_contact_number=data_json['emergency_contact_number'],
            emergency_contact_person=data_json['emergency_contact_person'],
            timestamp=time.time()
        )

        data = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/insert', methods=['POST'])
def insert_user():
    try:
        ref_id = ehs.generator()
        data = request.get_json()

        user = ehs.check_user(ref_id)
        if user["success"] is True:
            return {"success": False, "msg": "User already existed", "timestamp": time.time()}

        data = Data(
            ref_id=ref_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_initial=data['middle_initial'],
            emergency_contact_number=data['emergency_contact_number'],
            emergency_contact_person=data['emergency_contact_person'],
            result={
                "BLOOD_OXYGEN_LEVEL": "",
                "BODY_TEMPERATURE": "",
                "ECG_RESULT": "",
            },
            timestamp=time.time()
        )
        
        data = json.dumps(data, indent=4)

        resp = requests.put(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "ref_id": ref_id, "timestamp": time.time()}

@app.route('/send', methods=['GET'])
def send_sms():
    try:
        message = str(request.args['message'])
        number = str(request.args['number'])

        payload = {
            'message': message,
            'number': number,
            'apikey': ehs.SMS_API_KEY,
        }
        
        response = requests.request('POST', ehs.SMS_URL, data = payload)
    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": json.dumps(response.text, indent=4), "timestamp": time.time()}

@app.route('/start_test', methods=['POST'])
def tests():
    try:
        data = request.get_json()
        ref_id = data['ref_id']
        result = data['result']

        result = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{ehs.URL}/users/{ref_id}.json", headers=ehs.headers, data=result)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}