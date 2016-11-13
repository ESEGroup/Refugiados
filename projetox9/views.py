from projetox9 import app, Config
from .api import Api
from flask import render_template, request, redirect, url_for, session

class Views:
    api = Api()

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if (request.method == "GET"):
            return render_template('create-occurrence.html', googlemaps_autocomplete_key=Config.googlemaps_autocomplete_key)
        else:
            data = Views.api.set_occurrence(request.form["CPF"], request.form["occurrence"], request.form["date"], request.form["description"], request.form["lat"], request.form["lng"], request.form["place_name"])
            return render_template('occurrence.html', CPF=request.form["CPF"])

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if (session.get('logged')):
            return Views.manage()
        elif (request.method == 'POST' and request.form and request.form.get('CPF') and request.form.get('password')):
            CPF = request.form.get('CPF')
            password = request.form.get('password')
            logged, admin = Views.api.login(CPF, password)

            if (logged):
                session['logged'] = logged
                session['admin'] = admin
                session['CPF'] = request.form['CPF']
                return redirect(url_for('manage'))
        return render_template('login.html')

    @app.route('/manage')
    def manage():
        logged = session.get('logged')
        admin = session.get('admin')

        if (logged):
            occurrences = Views.api.get_occurrences()
            return render_template('manage.html', admin=admin, occurrences=occurrences)
        else:
            return redirect(url_for("login"))
