import re
from projetox9 import app

class Utils:
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
        if txt != None: return txt
        return ""

    @app.template_filter('len')
    def length(list):
        return len(list)

    @app.template_filter('bool')
    def bool(b):
        if b:
            return "Sim"
        return "Não"

    @app.template_filter('optional')
    def optional(txt):
        if (len(txt or "") == 0): return "-"
        return txt

    @app.template_filter('format_CPF')
    def format_CPF(CPF):
        CPF = Utils.clean_CPF(CPF)
        return "{0}.{1}.{2}-{3}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])

    def is_CPF_valid(CPF):
        return len(Utils.clean_CPF(CPF)) == 11

    def clean_CPF(CPF):
        CPF = CPF or ""
        return re.sub(r'\D','',CPF)

    @app.template_filter('get_date')
    def get_date(date):
        return date.split(" ")[0]

    @app.template_filter('get_time')
    def get_time(date):
        date = date.split(" ")

        if len(date) > 1:
            return date[1]
        return ""

    @app.template_filter('limit_size')
    def max_size_filter(txt):
        max_size=15
        if len(txt) > max_size:
            txt = re.sub(r'\ $', '', txt[:max_size-3])
            return txt + "..."
        return txt
