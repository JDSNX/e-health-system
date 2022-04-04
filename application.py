from flask import Flask
application = Flask(__name__)
application.config['TEMPLATES_AUTO_RELOAD'] = True

@application.route('/')
def hello_world():
    return 'Hello worlds!'
