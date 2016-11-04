import os
import sqlite3
from flask import Flask

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'projetox9.db'),
    SECRET_KEY='<dev_secret_key>',
    USERNAME='<username>',
    PASSWORD='<password>'
))
app.config.from_envvar('SETTINGS', silent=True)
