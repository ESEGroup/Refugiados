import re

class Utils:
    def title(txt):
        list = txt.split(" ")
        for t in list:
            if len(t) > 1:
                t = t[0].upper() + t[1:].lower()
        return "".join(list)

    def optional(txt):
        if (txt == None or txt == ""): return "-"
        return txt

    def format_CPF(CPF):
        CPF = Utils.clean_CPF(CPF)
        return "{0}.{1}.{2}-{3}".format(CPF[:3], CPF[3:6], CPF[6:9], CPF[9:])

    def is_CPF_valid(CPF):
        return len(Utils.clean_CPF(CPF)) == 11

    def clean_CPF(CPF):
        CPF = CPF or ""
        return re.sub(r'\D','',CPF)

    def get_date(date):
        return date.split(" ")[0]

    def get_time(date):
        date = date.split(" ")

        if len(date) > 1:
            return date[1]
        return ""
