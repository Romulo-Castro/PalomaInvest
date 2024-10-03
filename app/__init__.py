from flask import Flask
from flask_cors import CORS
from mvc_flask import FlaskMVC

def create_app():
    app = Flask(__name__)

    FlaskMVC(app)
    CORS(app)
    
    return app
