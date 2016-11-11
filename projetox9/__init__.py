from flask import Flask
app = Flask(__name__)

from .config import Config
config = Config()

from .server import server
