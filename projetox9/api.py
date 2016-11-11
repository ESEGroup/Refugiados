from .models import Models
from projetox9 import config
from urllib.request import urlopen
import json

class Api:
    def __init__(self):
        self.models = Models()

    def get_info_person(self, CPF):
        base_url = str(config.FakeSiga)
        path = '/api/Dados/findOne?filter={"where":{"CPF":"' + CPF + '"}}'
        f = urlopen(base_url + path)

        data = json.loads(f.read().decode('utf-8'))
        if (data["FuncionarioAdministrativo"]):
            user = self.models.Admin(data["CPF"], data["Nome"])
        elif (data["Professor"] or data["ProfessorVisitante"] or data["FuncionarioTerceirizado"]):
            user = self.models.Employee(data["CPF"], data["Nome"])
        else:
            user = self.model.User(data["CPF"], data["Nome"])
        return user

    def create_occurrence(self, CPF, occurrence, date, description):
        print(self.get_info_person(CPF))
