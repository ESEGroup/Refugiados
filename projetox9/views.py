from projetox9 import app, Config
from .api import Api
from .utils import Utils
from flask import render_template, request, redirect, url_for, session
import json

class Views:
    api = Api()

    @app.route('/')
    def create_occurrence():
        error = json.loads(request.args.get("error", "{}"))

        occurrence_types = Views.api.get_occurrence_types()
        return render_template('create-occurrence.html',
                error=error,
                googlemaps_key=Config.googlemaps_key,
                occurrence_types=occurrence_types)

    @app.route('/occurrence', methods=['GET', 'POST'])
    def occurrence():
        errors = {}
        admin = session.get("admin")
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

            status_list = Views.api.get_status_list()

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
                                request.args["protocol"].upper())

                if data:
                    return render_template('occurrence.html',
                                admin=admin,
                                protocol_number=data.protocol_number,
                                date=data.date,
                                occurrence=data.occurrence.name,
                                place_name=data.place_name,
                                description=data.description,
                                status=data.status,
                                feedback_date=data.feedback_date,
                                feedback=data.feedback,
                                status_list=status_list,
                                CPF=data.CPF,
                                name=data.name,
                                lat=data.location[0],
                                lng=data.location[1])
        return redirect(url_for('create_occurrence', error=json.dumps(errors), admin=admin))

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
        admin = session.get('admin')

        if request.method == "POST" and request.form.get("CPF") and request.form.get("password"):
            CPF, password = request.form.get('CPF'), request.form.get('password')
            user = Views.api.signup(CPF, password, admin)
            return redirect(url_for('manage'))
        return render_template('sign.html', title="Cadastro", path='signup', action="Cadastrar")

    @app.route('/manage')
    def manage():
        logged, admin = session.get('logged'), session.get('admin')
        if not logged:
            return redirect(url_for("login"))

        occurrences = Views.api.get_occurrences()
        employee = Views.api.get_users_not_approved(admin=admin)
        return render_template('manage.html',
                admin=admin,
                googlemaps_key=Config.googlemaps_key,
                employee=employee,
                occurrences=occurrences)

    @app.route('/approve')
    def approve():
        logged, admin = session.get('logged'), session.get('admin')
        if not logged:
            return redirect(url_for("login"))

        if request.args.get("pk") and request.args.get("CPF") and admin:
            is_approved = Views.api.approve_user(admin, request.args["pk"], request.args["CPF"])

        return redirect(url_for("manage"))

    @app.route('/update_occurrence', methods=["POST"])
    def update_occurrence():
        logged, admin = session.get('logged'), session.get('admin')
        if not logged:
            return redirect(url_for("login"))


        if request.form.get("CPF") and request.form.get("protocol") and \
            request.form.get("status") and request.form.get("feedback_date") and \
            request.form.get("feedback"):
                Views.api.update_occurrence(
                            request.form["CPF"],
                            request.form["protocol"],
                            request.form["status"],
                            request.form["feedback_date"],
                            request.form["feedback"])
        return redirect(url_for("manage"))
