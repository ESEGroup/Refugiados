from projetox9 import app, Config
from .api import Api
from .utils import Utils
from flask import render_template, request, redirect, url_for, session
import json

class Views:
    api = Api()

    @app.route('/')
    def create_occurrence():
        error = json.loads(request.args["error"]) if request.args.get("error") else {}
        return render_template('create-occurrence.html', googlemaps_autocomplete_key=Config.googlemaps_autocomplete_key, error=error)

    @app.route('/occurrence', methods=['GET', 'POST'])
    def occurrence():
        errors = {}
        if request.form or request.args:
            if request.form:
                inputs = ["CPF", "occurrence", "date", "lat", "lng", "place_name"]
                obj = request.form
            else:
                inputs = ["CPF", "protocol"]
                obj = request.args

            for i in inputs:
                if not obj.get(i):
                    errors[i] = True

            if not Utils.is_CPF_valid(obj.get("CPF")):
                errors["CPF"] = True

            if not errors:
                if request.form:
                    data = Views.api.set_occurrence(
                                request.form["CPF"],
                                request.form["occurrence"],
                                request.form["date"],
                                request.form["description"],
                                request.form["lat"],
                                request.form["lng"],
                                request.form["place_name"])
                else:
                    data = Views.api.get_occurrence(
                                request.args["CPF"],
                                request.args["protocol"].upper()[:10])

                return render_template('occurrence.html',
                            protocol_number=data.protocol_number,
                            date=data.date.split(" ")[0],
                            time=data.date.split(" ")[1],
                            occurrence=Utils.title(data.occurrence),
                            place_name=data.place_name,
                            description=Utils.title(Utils.optional(data.description)),
                            status=data.status,
                            feedback_date=Utils.optional(data.feedback_date),
                            feedback=Utils.optional(data.feedback),
                            CPF=Utils.format_CPF(data.CPF),
                            lat=data.location[0],
                            lng=data.location[1])
        return redirect(url_for('create_occurrence', error=json.dumps(errors)))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('logged'):
            return Views.manage()
        elif request.method == 'POST' and request.form and request.form.get('CPF') and request.form.get('password'):
            CPF = request.form.get('CPF')
            password = request.form.get('password')
            logged, admin = Views.api.login(CPF, password)

            if logged:
                session['logged'] = logged
                session['admin'] = admin
                session['CPF'] = request.form['CPF']
                return redirect(url_for('manage'))
        return render_template('login.html')

    @app.route('/manage')
    def manage():
        logged = session.get('logged')
        admin = session.get('admin')

        if logged:
            occurrences = Views.api.get_occurrences()
            return render_template('manage.html', admin=admin, occurrences=occurrences)
        else:
            return redirect(url_for("login"))


    @app.route('/signup', methods=["GET", "POST"])
    def create_account():
        logged = session.get('logged')
        admin = session.get('admin')

        if logged:
            if request.method == "POST":
                CPF, password = request.form.get("CPF"), request.form.get("password")
                if CPF and password:
                    success = Views.api.create_account(CPF, password, admin)
                    return redirect(url_for('manage'))
            else:
                return render_template('signup.html')
        else:
            return redirect(url_for("login"))
