from projetox9 import app, Config
from .api import Api
from .utils import Utils
from flask import render_template, request, redirect, url_for, session
import json
import re

class Views:
    api = Api()

    @app.route('/')
    def create_occurrence():
        try:
            error = json.loads(request.args.get("error", "{}"))
        except Exception as ex:
            error = {}

        occurrence_types = Views.api.get_occurrence_types()

        return render_template('create-occurrence.html',
               error=error,
               googlemaps_key=Config.googlemaps_key,
               occurrence_types=occurrence_types,
               logged = session.get("logged"))

    @app.route('/occurrence', methods=['GET', 'POST'])
    def occurrence():
        logged = session.get("logged")
        if request.form or request.args:
            if request.form:
                inputs = ["occurrence", "date", "lat", "lng", "place_name"]
                obj = request.form
            else:
                inputs = ["CPF", "protocol"]
                obj = request.args

            errors = { i : len(obj.get(i,"")) == 0 for i in inputs}
            errors["CPF"] = not Utils.is_CPF_valid(obj.get("CPF"))

            status_list = Views.api.get_status_list()

            if not any(errors.values()):
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
                                request.args["protocol"])

                if data:
                    return render_template('occurrence.html',
                                logged=logged,
                                googlemaps_key=Config.googlemaps_key,
                                protocol_number=data.protocol_number,
                                date=data.date,
                                occurrence=data.occurrence.name,
                                description=data.description,
                                status=data.status,
                                feedback_date=data.feedback_date,
                                feedback=data.feedback,
                                status_list=status_list,
                                CPF=data.CPF,
                                name=data.name,
                                lat=data.location.lat,
                                lng=data.location.lng,
                                place_name=data.location.place_name)

        return redirect(url_for('create_occurrence', error=json.dumps(errors)))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('logged'):
            return redirect(url_for('manage'))
        elif request.method == 'POST' and request.form and request.form.get('CPF') and request.form.get('password'):
            CPF, password = request.form['CPF'], request.form['password']
            session['logged'], session['admin'] = Views.api.login(CPF, password)
            return redirect(url_for('manage'))

        return render_template('sign.html', title="Login", path="login", action="Entrar")


    @app.route('/signup', methods=['GET', 'POST'])
    def create_account():
        logged, admin = session.get('logged'), session.get('admin')
        if not logged:
            return redirect(url_for('login'))

        if request.method == "POST" and request.form.get("CPF") and request.form.get("password"):
            CPF, password = request.form.get('CPF'), request.form.get('password')
            Views.api.signup(CPF, password, admin)
            return redirect(url_for('manage'))

        return render_template('sign.html',
                title="Cadastro",
                path=re.sub(r'^\/','',url_for('create_account')),
                action="Cadastrar")

    @app.route('/manage')
    def manage():
        if not session.get('logged'):
            return redirect(url_for("login"))
        admin = session.get("admin")

        occurrences = Views.api.get_occurrences()
        employees = Views.api.get_employees_not_approved(admin=admin)

        return render_template('manage.html',
                admin=admin,
                googlemaps_key=Config.googlemaps_key,
                employees=employees,
                occurrences=occurrences)

    @app.route('/approve')
    def approve():
        pk, CPF = request.args.get('pk'), request.args.get('CPF')
        admin = session.get('admin')

        if admin and pk and CPF:
            Views.api.approve_employee(admin, CPF, pk)

        return redirect(url_for("manage"))

    @app.route('/update_occurrence', methods=["POST"])
    def update_occurrence():
        if not session.get('logged'):
            return redirect(url_for("login"))

        f = request.form
        CPF, protocol, status = f.get("CPF"), f.get("protocol"), f.get("status")
        feedback, feedback_date = f.get("feedback"), f.get("feedback_date")

        if CPF and protocol and status and feedback and feedback_date:
            Views.api.update_occurrence(
                        CPF,
                        protocol,
                        status,
                        feedback_date,
                        feedback)

        return redirect(url_for("manage"))

    @app.route('/logout')
    def logout():
        session['logged'], session['admin'] = False, False

        return redirect(url_for('create_occurrence'))
