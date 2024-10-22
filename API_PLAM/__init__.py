from flask import Flask, request, jsonify
import fdb
import os
from dotenv import load_dotenv

fdb.load_api(os.path.join('C:\\Program Files\\Firebird\\Firebird_3_0\\bin\\fbclient.dll'))


load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PATH = os.getenv('DB_PATH')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
    
def create_app():
    
    app = Flask(__name__)
    
    from . views import views
    app.register_blueprint(views)
    
    return app
    



