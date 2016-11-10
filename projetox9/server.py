import os
from projetox9 import app

from .views import Views

class Server:
    def __init__(self):
        self.views = Views()

if __name__ == "__main__":
    app.run(debug=True)

