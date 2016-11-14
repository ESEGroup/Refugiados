from .models import Models
from .utils import Utils
from .config import Config
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json

class Api:
    models = Models()

    def get_occurrence_types(self):
        return Api.models.OccurrenceType.get_all()

    def get_occurrences(self):
        occurrences = Api.models.Occurrence.get_all()
        return occurrences

    def get_occurrence(self, CPF, protocol):
        return Api.models.Occurrence.get_one(CPF, protocol)

    def get_person_info(self, CPF):
        CPF = Utils.clean_CPF(CPF)
        base_url = str(Config.FakeSiga)
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

    def set_occurrence(self, CPF, occurrence, date, description, lat, lng, place_name):
        user = self.get_person_info(CPF)
        oc = Api.models.Occurrence(user, date, occurrence, description, lat, lng, place_name)
        oc.save()
        return(oc)

    def login(self, CPF, password):
        logged, admin = False, False
        tmp_user = Api.models.Employee.get_one(Utils.clean_CPF(CPF))
        if (tmp_user):
            user = Api.models.Employee.auth(tmp_user, password)
            logged = user.is_employee and user.is_approved

        return logged, logged and user.is_admin

    def signup(self, CPF, password, admin):
        tmp_user = self.get_person_info(CPF)
        user = Api.models.Employee.create(CPF=CPF, name=tmp_user.name, password=password, is_admin=tmp_user.is_admin)
        user.save()

        manager = Api.models.Employee.create(is_admin=admin, is_approved=True)
        user = manager.approve_user(user)

        return user
