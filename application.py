from flask import Flask
import time

application = Flask(__name__)

@application.route('/')
def index():
    return {"success": True, "timestamp": time.time()}
