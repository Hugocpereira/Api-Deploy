from flask import Flask, request, jsonify, render_template
import fdb
import os
import platform
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS

if platform.system() == "Windows":
    fdb.load_api(r"C:\Program Files\Firebird\Firebird_3_0\bin\fbclient.dll")
else:
    fdb.load_api("/usr/lib/x86_64-linux-gnu/libfbclient.so")  

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PATH = os.getenv('DB_PATH')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

def create_app():
    
    app = Flask(__name__)
    
    CORS(app, supports_credentials=True)
    
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    jwt = JWTManager(app)

    from . views import views
    app.register_blueprint(views)
    
    return app
    



