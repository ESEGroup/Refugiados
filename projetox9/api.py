from .models import Models
from projetox9 import Config
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json

class Api:
    models = Models()

    def get_occurrences(self):
        pass

    def get_occurrence(self, CPF, protocol):
        return Models.Occurrence(Models.User(CPF, ""), " ", "Lol", "", -22, -23, "kek", protocol)

    def get_person_info(self, CPF):
        base_url = str(Config.FakeSiga_url)
        path = '/api/Dados/findOne?filter={"where":{"CPF":"' + CPF + '"}}'
        try:
            f = urlopen(base_url + path)
        except HTTPError as e:
            return Api.models.User(CPF, None)
        except URLError as e:
            return Api.models.User(CPF, None)

        data = json.loads(f.read().decode('utf-8'))
        if data["FuncionarioAdministrativo"]:
            user = self.models.Admin(data["CPF"], data["Nome"])
        elif data["Professor"] or data["ProfessorVisitante"] or data["FuncionarioTerceirizado"]:
            user = self.models.Employee(data["CPF"], data["Nome"])
        else:
            user = self.model.User(data["CPF"], data["Nome"])
        return user

    def set_occurrence(self, CPF, occurrence, date, description, lat, lng, place_name):
        user = self.get_person_info(CPF.replace(".","").replace("-",""))
        oc = Models.Occurrence(user, date, occurrence, description, lat, lng, place_name)
        oc.save()
        return(oc)

    def login(self, CPF, password):
        return True, True
