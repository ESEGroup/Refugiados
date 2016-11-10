from projetox9 import app
from .api import Api
from flask import render_template, request

class Views:
    def __init__(self):
        self.api = Api()

        @app.route('/', methods=['GET', 'POST'])
        def home():
            if (not request.form):
                return render_template('cadastro-ocorrencia.html')
            return render_template('home.html', CPF=request.form["CPF"])
