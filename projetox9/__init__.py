from flask import Flask
app = Flask(__name__)

from os import getenv #, urandom
app.config['SECRET_KEY'] = getenv('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a22'
#app.config['SECRET_KEY'] = urandom(20)

from .config import Config
from .views import Views
