import pyrebase
from datetime import datetime

class Firebase:
    def __init__(self, ref_id, personal_info):
        self.ref_id = ref_id
        self.personal_info = personal_info

        self.firebaseConfig = {
            'apiKey': "AIzaSyBPMKxnV5DUSxYkmogrwLQx54yNjn6DEAE",
            'authDomain': "ae-keys-1f1e9.firebaseapp.com",
            'projectId': "ae-keys-1f1e9",
            'storageBucket': "ae-keys-1f1e9.appspot.com",
            'messagingSenderId': "252863936258",
            'appId': "1:252863936258:web:b7c48e521deb2381d9341b",
            'measurementId': "G-S4JRK5HLEY",
            "databaseURL" : "https://ae-keys-1f1e9-default-rtdb.asia-southeast1.firebasedatabase.app/"
        }

        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = self.firebase.database()

        super().__init__()

    def get_all(self):
        try:
            rows = self.db.child("users").get().val()
        except Exception as e:
            return {"msg": e}

        return {"rows": rows}

    def get_user(self):
        try:
            rows = self.db.child("users").order_by_child("ref_id").equal_to(self.ref_id).get().val()
            
            if not rows:
                return {"rows": "user not found!"}

        except Exception as e:
            return {"msg": e}

        return {"rows": rows}

def noquote(s):
    return s

pyrebase.pyrebase.quote = noquote
