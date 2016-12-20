import re
from ..projetox9 import app, Config
from datetime import datetime
import json

class Utils:
    @app.template_filter('json')
    def to_json(obj):
        return json.dumps(obj)

    @app.template_filter('len')
    def length(list):
        return len(list)

    @app.template_filter('list')
    def to_list(l):
        return list(l)

    @app.template_filter('bool')
    def bool(b):
        return Config.bool_translation[bool(b)]

    @app.template_filter('title')
    def title(txt):
        list = txt.split(" ")
        ret = []
        for t in list:
            if len(t) > 1:
                ret += [t[0].upper() + t[1:].lower()]
            else:
                ret += [t]
        return " ".join(ret)

    @app.template_filter('empty')
    def empty(txt):
        if str(txt) != "None":
            return txt

        return ""

    @app.template_filter('optional')
    def optional(txt):
        if (len(Utils.empty(txt)) > 0):
            return txt

        return "-"

    @app.template_filter('limit_size')
    def max_size_filter(txt):
        if len(txt) > Config.frontend_max_len:
            txt = re.sub(r'\ $', '', txt[:Config.frontend_max_len-3]) + "..."

        return txt

    @app.template_filter('get_date')
    def get_date(date):
        return date.split(" ")[0]

    @app.template_filter('get_time')
    def get_time(date):
        date = date.split(" ")
        date.pop(0)
        return date[0] if date else ""

    @app.template_filter('format_CPF')
    def format_CPF(CPF):
        CPF = Utils.clean_CPF(CPF)
        return "{0}.{1}.{2}-{3}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])

    def is_CPF_valid(CPF):
        return len(Utils.clean_CPF(CPF)) == 11

    def clean_CPF(CPF):
        CPF = CPF or ""
        return re.sub(r'\D','',CPF)

    @app.template_filter('name_or_input')
    def name_or_input(value):
        if value in ["", "-", "None"]:
            return "<input type='text' name='name'>"
        else:
            return value

    @app.template_filter('to_date')
    def to_date(value):
        return datetime.strptime(value, "%d/%m/%Y %H:%M")

    def format_date(value):
        return datetime.strftime(value, "%d/%m/%Y %H:%M")

    def to_timestamp(date):
        return Utils.to_date(date).timestamp()

    def from_timestamp(date):
        return Utils.format_date(datetime.fromtimestamp(date))

    def get_month(date):
        return date[3:5]
