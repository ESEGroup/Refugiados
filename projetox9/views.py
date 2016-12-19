from ..projetox9 import app, Config
from .api import Api
from .utils import Utils
from flask import render_template, request, redirect, url_for, session
import json
import re
from datetime import datetime, timedelta

class Views:
    api = Api()

    @app.route('/')
    def create_occurrence():
        logged = session.get("logged")

        request.args = request.args or {}
        error        = json.loads(request.args.get("error") or "{}")

        occurrence_types = Views.api.get_occurrence_types()
        
        message             = session.get('messages')
        session['messages'] = None
        if message != None:
            return render_template('create-occurrence.html',
                   googlemaps_key   = Config.googlemaps_key,
                   error            = error,
                   logged           = logged,
                   occurrence_types = occurrence_types,
                   message          = message)

        return render_template('create-occurrence.html',
               googlemaps_key   = Config.googlemaps_key,
               error            = error,
               logged           = logged,
               occurrence_types = occurrence_types)

    @app.route('/occurrence', methods=['GET', 'POST'])
    def occurrence():
        logged = session.get("logged")
        form   = request.form or request.args
        errors = {}

        if form:
            fields = {"POST": ["CPF",
                               "name",
                               "occurrence",
                               "date",
                               "description",
                               "lat",
                               "lng",
                               "place_name"],
                     "GET": ["CPF",
                             "protocol"]
                     }

            # Validate form
            errors = { field: len(form.get(field,"")) == 0 for field in fields[request.method]}
            errors["CPF"] = not Utils.is_CPF_valid(form.get("CPF"))

            status_list = Views.api.get_status_list()

            if not any(errors.values()):
                api_function = {"POST": Views.api.set_occurrence,
                                "GET":  Views.api.get_occurrence}
                args = (form[field] for field in fields[request.method])

                data = api_function[request.method](*args)

                if data:
                    return render_template('occurrence.html',
                                logged=logged,
                                googlemaps_key  = Config.googlemaps_key,
                                protocol_number = data.protocol_number,
                                date            = data.date,
                                occurrence      = data.occurrence.name,
                                description     = data.description,
                                status          = data.status,
                                feedback_date   = data.feedback_date,
                                feedback        = data.feedback,
                                status_list     = status_list,
                                CPF             = data.CPF,
                                name            = data.name,
                                lat             = data.location.lat,
                                lng             = data.location.lng,
                                place_name      = data.location.place_name)
            else:
                session['messages'] = "Campos obrigatórios não preenchidos. Tente novamente"
                return redirect(url_for('create_occurrence', error=json.dumps(errors)))
        
        session['messages'] = "Ocorrência não encontrada.</p><br><p> Verifique os dados digitados."
        return redirect(url_for('create_occurrence', error=json.dumps(errors)))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = request.form or {}
        if session.get('logged'):
            return redirect(url_for('manage'))
        elif request.method == 'POST' and form.get('CPF') and form.get('password'):
            session['logged'], session['admin'] = Views.api.login(form.get("CPF"),
                                                                  form.get("password"))

            return redirect(url_for('manage'))

        return render_template('sign.html',
                               title  = "Login",
                               path   = re.sub(r'^\/','',url_for("login")),
                               action = "Entrar")


    @app.route('/signup', methods=['GET', 'POST'])
    def create_account():
        logged, admin = session.get('logged'), session.get('admin')
        if not logged:
            return redirect(url_for('login'))

        if request.method == "POST" and request.form.get("CPF") and request.form.get("password"):
            CPF, password = request.form.get('CPF'), request.form.get('password')
            Views.api.signup(CPF, password, admin)
            session['messages'] = "Usuário " + CPF + " cadastrado com sucesso!"

            return redirect(url_for('manage'))

        return render_template('sign.html',
                title  = "Cadastro",
                path   = re.sub(r'^\/','',url_for('create_account')),
                action = "Cadastrar",
                logged = logged)

    @app.route('/manage')
    def manage():
        logged, admin = session.get("logged"), session.get("admin")
        if not logged:
            return redirect(url_for("login"))

        occurrences = Views.api.get_occurrences()
        employees   = Views.api.get_employees_not_approved(admin=admin)

        date_range = Utils.format_date(datetime.now() - timedelta(minutes=Config.current_occurrences_range_minutes))
        
        message = session.get('messages')
        session['messages'] = None

        if message != None:
            return render_template('manage.html',
                    admin                  = admin,
                    googlemaps_key         = Config.googlemaps_key,
                    employees              = employees,
                    occurrences            = occurrences,
                    occurrences_date_range = date_range,
                    message                = message)

        return render_template('manage.html',
                    admin                  = admin,
                    googlemaps_key         = Config.googlemaps_key,
                    employees              = employees,
                    occurrences            = occurrences,
                    occurrences_date_range = date_range)

    @app.route('/charts')
    def chats():
        logged = session.get("logged")
        if not logged:
            return redirect(url_for("login"))

        charts_dataset = Views.api.get_charts_dataset()
        return render_template('charts.html')

    @app.route('/approve')
    def approve():
        admin = session.get('admin')

        request.args = request.args or {}
        pk, CPF      = request.args.get('pk'), request.args.get('CPF')
        name         = request.args.get('name')

        Views.api.approve_employee(admin, CPF, pk, name)

        return redirect(url_for("manage"))

    @app.route('/update_occurrence', methods=["POST"])
    def update_occurrence():
        if not session.get('logged'):
            return redirect(url_for("login"))

        form = request.form or {}
        fields = ["CPF",
                  "protocol",
                  "status",
                  "feedback_date",
                  "feedback"]

        args = [form.get(field) for field in fields]

        Views.api.update_occurrence(*args)

        return redirect(url_for("manage"))

    @app.route('/logout')
    def logout():
        session['logged'], session['admin'] = False, False

        return redirect(url_for('create_occurrence'))
