import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from projetox9 import Config
from .models import Models
from .utils import Utils

class Api:
    models = Models()

    def get_occurrence_types(self):
        return Api.models.OccurrenceType.get_all()

    def get_occurrence_type(self, pk):
        return Api.models.OccurrenceType.get_one_or_empty(pk)

    def get_occurrences(self):
        occurrences = Api.models.Occurrence.get_all()
        return occurrences

    def get_occurrence(self, CPF, protocol):
        return Api.models.Occurrence.get_one(Utils.clean_CPF(CPF), protocol)

    def set_occurrence(self, CPF, oc_type_pk, date, description, lat, lng, place_name):
        user = self.get_person_info(Utils.clean_CPF(CPF))
        occurrence_type = self.get_occurrence_type(oc_type_pk)

        oc = Api.models.Occurrence(user.CPF, user.name, date, occurrence_type, description, lat, lng, place_name)
        oc.save()
        return(oc)

    def login(self, CPF, password):
        user = Api.models.Employee.get_one_or_empty(Utils.clean_CPF(CPF))
        user = Api.models.Employee.auth(user, password)

        logged = user.is_employee and user.is_approved
        return logged, logged and user.is_admin

    def signup(self, CPF, password, admin):
        user = self.get_person_info(Utils.clean_CPF(CPF))
        user = Api.models.Employee.create(CPF=user.CPF, name=user.name, is_admin=user.is_admin, password=password)
        user.save()

        manager = Api.models.Employee.create(is_admin=admin, is_approved=True)
        user = manager.approve_user(user) or user

        return user

    # FakeSiga
    def get_person_info(self, CPF):
        base_url = str(Config.FakeSiga)
        path = '/api/Dados/findOne?filter={"where":{"CPF":"' + CPF + '"}}'

        try:
            f = urlopen(base_url + path)
        except HTTPError as e:
            return Api.models.User(CPF, None)
        except URLError as e:
            return Api.models.User(CPF, None)

        data = json.loads(f.read().decode('utf-8'))

        is_admin = data["FuncionarioAdministrativo"]
        is_employee = data["Professor"] or data["ProfessorVisitante"] or data["FuncionarioTerceirizado"] or is_admin

        return Api.models.User.create(data["CPF"], data["Nome"], is_employee, is_admin)
