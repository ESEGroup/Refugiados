import os
from projetox9 import app, config
from .views import Views

class Server:
    def __init__(self):
        self.views = Views()

server = Server()

if __name__ == "__main__":
    app.run(host=config.projetox9["host"], port=config.projetox9["port"], debug=True)
