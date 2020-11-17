from flask import Flask
import os
# from config import STORE_PATH

app = Flask(__name__)
# BASEDIR = os.path.dirname(os.path.abspath(__file__))
# app.config['FILES_UPLOAD'] = STORE_PATH


from . import routes