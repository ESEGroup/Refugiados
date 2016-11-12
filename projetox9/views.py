from projetox9 import app
from .api import Api
from flask import render_template, request

class Views:
    def __init__(self):
        self.api = Api()

        @app.route('/', methods=['GET', 'POST'])
        def home():
            if (not request.form):
                return render_template('create-occurrence.html')
            else:
                self.api.create_occurrence(request.form["CPF"], request.form["occurrence"], request.form["date"], request.form["description"])
                return render_template('home.html', CPF=request.form["CPF"])

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if (request.form and request.form.get('CPF') and request.form.get('password')):
                CPF = request.form.get('CPF')
                password = request.form.get('password')
                logged, admin = self.api.login(CPF, password)

                if (logged):
                    resp = make_response(render_template('admin.html', logged=logged, admin=admin)
                else:
                    resp = make_response(render_template('login.html'))

                resp.set_cookie('logged', logged)
                resp.set_cookie('admin', admin)
                return resp
            else:
                return render_template('login.html')

        @app.require('/admin')
        def admin():
            logged = request.cookies.get('logged')
            admin = request.cookies.get('admin')

            if (logged):
                occurrences = self.api.get_occurrences()
                return render_template('admin.html', admin=admin, occurrences=occurrences)
            else:
                return Views.login()
