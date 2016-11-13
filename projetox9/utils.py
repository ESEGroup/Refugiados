import re

class Utils:
    def title(txt):
        l = txt.split(" ")
        ret = ""
        for t in l:
            ret += t[0].upper() + t[1:].lower()
        return txt[0].upper() + txt[1:].lower()

    def format_CPF(CPF):
        CPF = CPF.replace(".","").replace("-","")
        CPF = re.sub(r'[a-zA-Z]','', CPF)
        return CPF[:3] + "." + CPF[3:6:] + "." + CPF[6:9] + "-" + CPF[9:]

    def CPF_is_valid(CPF):
        ret = len(Utils.format_CPF(CPF)) == 14
        return ret

    def optional(txt):
        if (txt == None): return "-"
        return txt

