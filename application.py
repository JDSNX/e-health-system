import json
import time
import requests
import uuid

from requests.structures import CaseInsensitiveDict
from flask import Flask, request, render_template

app = Flask(__name__)

sms_url = 'https://api.semaphore.co/api/v4/messages'
headers = CaseInsensitiveDict
headers = {"Content-Type": "application.json"}

def generator():
    return uuid.uuid4().hex.upper()[0:5]

def check_user(ref_id=None):
    try:
        resp = requests.get(url=f"{url}/users/{ref_id}.json", headers=headers)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.json(), "timestamp": time.time()}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def get_all():
    if request.method == 'POST':
        return "Nuh-uh!"

    if request.method == 'GET':
        try:
            resp = requests.get(url=f"{url}/users.json", headers=headers)

        except Exception as e:
            return {"success": False, "msg": e, "timestamp": time.time()}

        return {"success": True, "result": resp.json(), "timestamp": time.time()}

@app.route('/get_user', methods=['GET'])
def get_user(ref_id=None):
    try:
        ref_id = str(request.args['ref_id'])
        resp = requests.get(url=f"{url}/users/{ref_id}.json", headers=headers)

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

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=data)

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

        resp = requests.delete(url=f"{url}/users/{ref_id}.json", headers=headers)

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        data_json = request.get_json()
        ref_id = data_json['ref_id']
        first_name = data_json['first_name']
        last_name = data_json['last_name']
        middle_initial = data_json['middle_initial']
        emergency_contact_number = data_json['emergency_contact_number']
        emergency_contact_person = data_json['emergency_contact_person']

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "msg": "User not found!", "timestamp": time.time()}

        data = {
            "first_name": first_name, 
            "last_name": last_name, 
            "middle_initial": middle_initial, 
            "emergency_contact_number": emergency_contact_number, 
            "emergency_contact_person": emergency_contact_person, 
            "timestamp": time.time()
        }

        data = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/insert', methods=['POST'])
def insert_user():
    try:
        ref_id = generator()
        data = request.get_json()
        

        first_name = data['first_name']
        last_name = data['last_name']
        middle_initial = data['middle_initial']
        emergency_contact_number = data['emergency_contact_number']
        emergency_contact_person = data['emergency_contact_person']
        

        user = check_user(ref_id)
        if user["success"] is True:
            return {"success": False, "msg": "User already existed", "timestamp": time.time()}

        data = {
            "ref_id": ref_id, 
            "first_name": first_name,
            "last_name": last_name, 
            "middle_initial": middle_initial, 
            "emergency_contact_person": emergency_contact_person, 
            "emergency_contact_number": emergency_contact_number, 
            "result": {
                "BLOOD_OXYGEN_LEVEL": "",
                "BODY_TEMPERATURE": "",
                "ECG_RESULT": "",
            }, 
            "password": "",
            "timestamp": time.time()
        }
        data = json.dumps(data, indent=4)

        resp = requests.put(url=f"{url}/users/{ref_id}.json", headers=headers, data=data)

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
            'apikey': sms_api_key,
        }
        
        response = requests.request('POST', sms_url, data = payload)
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

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=result)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

if __name__ == "__main__":
    app.secret_key = "ItsASecret"
    app.run(debug=True, use_debugger=True, use_reloader=False)
