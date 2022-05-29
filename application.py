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
    return "- EHMS-API -"

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

@app.route('/update_pass', methods=['GET'])
def update_pass():
    try:
        ref_id = str(request.args['ref_id'])
        password = str(request.args['password'])

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

@app.route('/update_user', methods=['GET'])
def update_user():
    try:
        ref_id = str(request.args['ref_id'])
        first_name = str(request.args['first_name'])
        last_name = str(request.args['last_name'])
        middle_initial = str(request.args['middle_initial'])
        emergency_contact_number_1 = str(request.args['emergency_contact_number_1'])
        emergency_contact_person_1 = str(request.args['emergency_contact_person_1'])
        emergency_contact_number_2 = str(request.args['emergency_contact_number_2'])
        emergency_contact_person_2 = str(request.args['emergency_contact_person_2'])
        emergency_contact_number_3 = str(request.args['emergency_contact_number_3'])
        emergency_contact_person_3 = str(request.args['emergency_contact_person_3'])

        user = get_user(ref_id)
        if user["success"] is False:
            return {"success": False, "msg": "User not found!", "timestamp": time.time()}

        data = {
            "first_name": first_name, 
            "last_name": last_name, 
            "middle_initial": middle_initial, 
            "emergency_contact_number_1": emergency_contact_number_1, 
            "emergency_contact_person_1": emergency_contact_person_1, 
            "emergency_contact_number_2": emergency_contact_number_2, 
            "emergency_contact_person_2": emergency_contact_person_2, 
            "emergency_contact_number_3": emergency_contact_number_3, 
            "emergency_contact_person_3": emergency_contact_person_3, 
            "timestamp": time.time()
        }

        data = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=data)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/insert', methods=['GET'])
def insert_user():
    try:
        ref_id = generator()
        first_name = str(request.args['first_name'])
        last_name = str(request.args['last_name'])
        middle_initial = str(request.args['middle_initial'])
        
        emergency_contact_number_1 = str(request.args['emergency_contact_number_1'])
        emergency_contact_person_1 = str(request.args['emergency_contact_person_1'])
        emergency_contact_number_2 = str(request.args['emergency_contact_number_2'])
        emergency_contact_person_2 = str(request.args['emergency_contact_person_2'])
        emergency_contact_number_3 = str(request.args['emergency_contact_number_3'])
        emergency_contact_person_3 = str(request.args['emergency_contact_person_3'])
        

        user = check_user(ref_id)
        if user["success"] is True:
            return {"success": False, "msg": "User already existed", "timestamp": time.time()}

        data = {
            "ref_id": ref_id, 
            "first_name": first_name,
            "last_name": last_name, 
            "middle_initial": middle_initial, 
            "emergency_contact_person_1": emergency_contact_person_1, 
            "emergency_contact_number_1": emergency_contact_number_1,
            "emergency_contact_person_2": emergency_contact_person_2, 
            "emergency_contact_number_2": emergency_contact_number_2, 
            "emergency_contact_person_3": emergency_contact_person_3, 
            "emergency_contact_number_3": emergency_contact_number_3,  
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
        data['timestamp'] = time.time()

        result = json.dumps(data, indent=4)

        resp = requests.patch(url=f"{url}/users/{ref_id}.json", headers=headers, data=result)

        if resp.json() is None:
            return {"success": False, "timestamp": time.time()}

    except Exception as e:
        return {"success": False, "msg": e, "timestamp": time.time()}

    return {"success": True, "result": resp.reason, "timestamp": time.time()}

@app.route('/empty_image', methods=['GET'])
def image():
    image64_1 = "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" 
    image64_2 = "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"
    image64_3 = "EnHFJrZMPKtaH0McSqiJMOS+nJ3lj+8H8YUQXDooTyMph4qqEC01zrg3XLfHJfYtzr6wG5eyp4mDorf6EO3KV7vnqz3fK6ZVL/qfmMRWRKtaNyGWqfX9axNPunsEl5/OcmHiOPyQ1a1yxdYB5zH9CDE7DGBL7Ju3faGnL9Zcv4uYoCg6+RI/zvfSVa9YDlam/4lJbJk4VrVkNmAa6N5ThFZwwXUe0PYxHITJoBbnIFp7qoOl46MMauxbln3BGhkLP2iSCFaz+o8b7cHKb8061DDkaherWw55k+BgUIWKt5bVNFX/MYYQSue31GvVXi+Vla4UyTu1n3KNIhWVV6Fm0GRGSg+s/jtwGcjq1nnow7thKzLL6zKz3NQQW+96DHp4Rlhh37ztC938DPHB5hTFoP6F+GmVJl07N2EWNsZYIgKxpSnOQ6c3vwmd5UbSmTZlYSIQXNLpSXibDBx1X+dbf9cOPotHImy8cYUWX8HP7JBwwqZcZMk/9Hlq0hFXBmJj4dgZ35N+uFRHR8/ecz0G1di3WPvCEwJV6/4coercx7jfEF1zz74GYYQxiC0Tx4zbeSQNIpTgutvo9JYeGv2iFWAaSy+D4TSA8IrpcER5jpUJG06L2IpXbH3yYPt5oeV77smGIe07xb7B7As/uTU/J3IpszCia6KLHL6OF5LJnhGZOt3w6tu3by9+Sc8A+Rr4WT/ruUfRoOnffQiuKxPRrJKGUp6r+HItOqI7hV7DCT8FfowPhHLER1M3ZKByPTv/rrQZZo9j0G/PRQlg37ztu+W5vjl8Fpk8De3YSlm0E7fyec/qVXRt40iFr48J3uT7Htd9iR5kbU3Xla3Qzq4sY1cRzj64XOGSd56pyFpF9t7SKU83slO6ii++ivEUet27d27ChtWWvMIRMzIL7Pr8PekLx4WVq4/+/7qDI45987avT+Zk8YMu/pb6Gz5WuFphBwPzYjZCdahD70+KNiGAioGrgf+sZKUZ6dkMq4g7gXsdLEZm+Ew6UQqtiCYgDknVGiU+BPCx7m8pAp2pPPZwqwX2Ld6+EHddmWtoXWmCS/odHyni96llgcRWBE7lXezhUgMKLmlMb1Vk3SfUEWyKriHKIXah1aaCvgk9CUEXFl29kFXfWw+3mhVUrD76/4cuzjj2zdu+EL0ol4n/LyUKLsM+7ezFVmiHLolGtaPgktjt93rQ3SphR/Ney+HdDg5J9EIroro5CXHIM0ThKMshlNkPvvqOPsJ1FxYTXNg3b/tC/P1qcYJLJ3pcn/U5opoFEFs6kxByX8pNSpv1egouWc06yinjj9isuSTE7XPGQqs9G+Mq4CPIPjkOIowPacs+Dqe8yDmUVDOg+prsm2Ff7AvR1hWpJ4+zIJe4wuXaH0ZshRBbJvzMfZWg0OgquGSw/qCrWVnOuGn2yHcdHZOkhFZEdRSxFV+9b49N8ME8c9HqIwPXjc1RGtg3b/tCdEJr/5lxtjTBtaJGpMlL2QhDOnI3qaag7JClUJaCJyUMAGJDncEUWx5mJrS+r24173dlwiWROeFsjGhFuI86IYlSZrEdizGAgzUz/s7zm2Ff7AvRMntBlIvgMhyFAq3P2Xy8iu25Xj/TGfo4Q+mlwSxlg4t42LbCJXuZjkqaadOZ4PET5ZGs0IqorrK6FaEIN36yRwlnOc3u6thz5ul2d31CuNW+N9g3T/tCNHVF/IYukxqlJs0YmhVF4FlsBXbg7nI4WG+L4BJhcVTiRt2N5BlXmQkt3471Nhhk4sTnjPosh/09+g5zj7esAv0W+8ZvX0irD0VwIbYQW6V2kBsCIwthQXlE4Vg/5lBDNSGuul4bf6sfEoVQp+yQ67PXxl9ExU7HimDfvO0LwevLtqQYXQRXzmGjnK2ZKG+eqOQhQwgfcusgEVn5l4fuTbs1/vYhPGZi2JsQI1VzffXskI9TC1MO4IgL59gX+0KU9eW5pBgvcab1LcfkY67F1iqTuuOsnPpG3b1+xnELBQ4jpErIusu+rUhFuPF7PEByKyCBHPGbIfbyYN+87QtBx9Jd6suxCAddOMhFgI6M+6OYVhkUlfQ3Xx1evYhRbM3pZyBRfJ2/s3Vw4YDjaKk814vWIY/e0dAN8L4dceEc+2JfiLbOnA7UTv5u/t4ikzD7ysM9OCLBEa+3VPQjEy6E8JoU1pAqns/f2cYYK0RZL6RP873q2ToaVazlonsyvgYYbz4PGYaHffO2L3hn6LZ0IiJC2kqqE5Lql7s+auKhxORtwcSWYVULIKaBwgZCCeMVXOIU3wW49UUzUNcxzeyKwyPP1PzzU4DbywpUhX2xL0Qr0F3sexbBf2HWoYVJiS59Vh+TuDU10K/YGgd6lgdirCEDp1pmVG8D3X6MBaJmGui+sn9hqY5MaMdBymClzxTEBg5nb7Fv3vYF96LCtVBOSnTpipb4FAcebofY8iW2tOKF6iQRWpAL80D3PcjhLJ6MhbgMZp8D3V6cjE9N/VjqngjfTsNYVzu+mLBh6gvsi30hSmYe686m6JrHOG5qiPA/noQWPrhjHqd+Hwd8FgwNuSB1+VOge0sbZr9CvFRqo1BHBMh9vzYDuZwPVbk+PF4df3nn48DlLiF+U+yLfSE+BkyK0Ud0yX1P9eiWuYzfoXIH6ILHRNvUgc/2Q74Ev2IrlLonhBCyQTqtgGduyaDF8Qnx1o17DbWqTbgVAKPOsTjld1pfBnMwdP/QRJ3fw0iK3kt4GfbN277gjBjGLKnLMkn6Scfvur1c1y3NLNpeIfqNOVXQr9gaB3oOhBbkxtyEWd0ijDB+wdXur/kSweMcbDgYd9oXy8rosmtGNw3BGen4MY7IAW/56HqFB/uWY18YXGicR1inDvU602e81Xaz0s/7PnVu48DdkX7KdRzB+yK2HPPq27dvmxXhW6DneM/KFmQ2gEhn+m+g278lJCCJOiID3GkCj3rzjLDfi/zZr5q2MMW+2LenDV36RJeaxbLkPnBfBcxewq/xYF4O3Y+5LQXrIx3VqbHZ4fDhl2jK6lWf37159IBBQGhBbmgoocwkHwS4vbTlOVaIvo5MddXgMPJHPU60iGU2+hz7Yl+IlnHiQsvo8x8n/PwV1dA9rx8p7xBcYwbIlFCTCIQSpuVs3FIMgyMTHeMI9vFg37ztCzugE+0fKIlgXBEFU47YqjEDZEqouo3YSsfZEGdRNkU/UBqDIWU5icERx7552xcGaSPz5uN32kiQdlRRDIgtAMRWP44p+qScjZVZr4DgbAzjQIy7Jn/AvtgXomgjS/VBWQX2x4xVrTBiK0Rc+QOdJmQ8gNyHGjw43DhJZwOHPFNHHPsitODFNrLSNnJDaTjnpvTkLEHEVsDkGDUmgMwJVcdHFD2CC0cc+2JfSKgPlJTq0kY+UxpO29KUYgggtgI6ZnScgNhyAytbaQsuwmm6c5eKI45987YvDNZOJMvke8PEhAsmhA+WJ7ZqTACZE8pBQGwhuEpAyugoJUcc++ZtXxisnSwM+7iG5gMHgIcVW+NAjQmjQ+4DxsqEmZ3bp/STrjcSTiOOxhWl8SRSNkmm/8a+edsXhhs/tZ1cUhqDCK05xRBWbIVwzJitgFIIMStLRsI8nI2p4RyabXyUskndEce+edsXBmsnlVmnh8dvRGglLbZCZCJcUfxQCHWIm/7x55+sbuXhaMxxNH4g+3d+b8pkhn2xLxTVDy51leujYS8XQis1sRXQISMGG0phFei+7NvKyNEw63DvkrN0ybtnuX8H++ZtXxi0rYgQHxlCcF9CBOk7hFYcvAnokNGhAmLLLaxs5eVkSEjV+R9//ikbx2UAPSjk1WW1Y5r7"
    image64_4 = "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"
    image64_5 = "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"
    image64_6 = "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"
    image64_7 = "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"
    return image64_1+image64_2+image64_3+image64_4+image64_5+image64_6+image64_7

if __name__ == "__main__":
    app.secret_key = "ItsASecret"
    app.run(debug=True, use_debugger=True, use_reloader=False)
