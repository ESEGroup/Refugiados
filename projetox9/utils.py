import re

class Utils:
    def title(txt):
        l = txt.split(" ")
        ret = ""
        for t in l:
            if len(t) < 2:
                ret += t
            else:
                ret += t[0].upper() + t[1:].lower()
        return ret

    def format_CPF(CPF):
        CPF = CPF.replace(".","").replace("-","")
        CPF = re.sub(r'[a-zA-Z]','', CPF)
        return CPF[:3] + "." + CPF[3:6:] + "." + CPF[6:9] + "-" + CPF[9:]

    def is_CPF_valid(CPF):
        if type(CPF) != type(""):
            return CPF
        ret = len(Utils.format_CPF(CPF)) == 14
        return ret

    def optional(txt):
        if (txt == None or txt == ""): return "-"
        return txt

