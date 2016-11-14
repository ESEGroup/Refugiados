from .models import Models
from .utils import Utils
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
        CPF = Utils.clean_CPF(CPF)
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
            user = Api.models.Admin(data["CPF"], data["Nome"])
        elif data["Professor"] or data["ProfessorVisitante"] or data["FuncionarioTerceirizado"]:
            user = Api.models.Employee(data["CPF"], data["Nome"])
        else:
            user = Api.models.User(data["CPF"], data["Nome"])
        return user

    def get_occurrence_type(self, occurrence):
        return occurrence

    def set_occurrence(self, CPF, occurrence, date, description, lat, lng, place_name):
        user = self.get_person_info(CPF)
        oc_type = self.get_occurrence_type(occurrence)
        oc = Api.models.Occurrence(user, date, oc_type, description, lat, lng, place_name)
        oc.save()
        return(oc)

    def login(self, CPF, password):
        return True, True

    def create_account(self, CPF, password, admin):
        tmp_user = self.get_person_info(CPF)
        if (tmp_user.is_admin):
            user = Api.models.Admin(CPF, tmp_user.name, password, admin)
        else:
            user = Api.models.Employee(CPF, tmp_user.name, password, admin)
        return user
