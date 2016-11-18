import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from projetox9 import Config
from .models import Models, Status
from .utils import Utils

class Api:
    models = Models()

    def get_occurrence_types(self):
        return self.models.OccurrenceType.get_all()

    def get_occurrence_type(self, pk):
        return self.models.OccurrenceType.get_one_or_empty(pk)

    def get_occurrences(self):
        occurrences = self.models.Occurrence.get_all()
        return occurrences

    def get_occurrence(self, CPF, protocol):
        return self.models.Occurrence.get_one(Utils.clean_CPF(CPF), protocol.upper())

    def get_users_not_approved(self, admin=True):
        if not admin: return
        return self.models.Employee.get_all({"is_approved":False})

    def set_occurrence(self, CPF, oc_type_pk, date, description, lat, lng, place_name):
        user = self.get_person_info(Utils.clean_CPF(CPF))
        occurrence_type = self.get_occurrence_type(oc_type_pk)

        oc = self.models.Occurrence(user.CPF, user.name, date, occurrence_type, description, lat, lng, place_name)
        oc.save()
        return oc

    def update_occurrence(self, CPF, protocol, status, feedback_date, feedback):
        occurrence = self.models.Occurrence.get_one(CPF, protocol)
        occurrence.status = status
        occurrence.feedback_date = feedback_date
        occurrence.feedback = feedback
        occurrence.update()

    def login(self, CPF, password):
        user = self.models.Employee.get_one_or_empty(Utils.clean_CPF(CPF))
        user = self.models.Employee.auth(user, password)

        return user.is_approved, user.is_approved and user.is_admin

    def signup(self, CPF, password, admin):
        user = self.get_person_info(Utils.clean_CPF(CPF))
        user = self.models.Employee.create(CPF=user.CPF, name=user.name, is_admin=user.is_admin, password=password)
        user.save()

        manager = self.models.Employee.create(is_admin=admin, is_approved=admin)
        user = manager.approve_user(user) or user

        return user

    def approve_user(self, admin, CPF, pk):
        user = self.models.Employee.get_one_or_empty(CPF, pk=pk)

        manager = self.models.Employee.create(is_admin=admin, is_approved=admin)
        user = manager.approve_user(user) or user

        return user.is_approved

    def get_status_list(self):
        return [getattr(Status,s) for s in Status.__dict__ if not s.startswith("__")]

    # FakeSiga
    def get_person_info(self, CPF):
        base_url = str(Config.FakeSiga)
        path = '/api/Dados/findOne?filter={"where":{"CPF":"' + CPF + '"}}'

        try:
            f = urlopen(base_url + path)
        except HTTPError as e:
            return self.models.User(CPF, None)
        except URLError as e:
            return self.models.User(CPF, None)

        data = json.loads(f.read().decode('utf-8'))

        is_admin = data["FuncionarioAdministrativo"]
        is_employee = data["Professor"] or data["ProfessorVisitante"] or data["FuncionarioTerceirizado"] or is_admin

        return self.models.User.create(data["CPF"], data["Nome"], is_employee, is_admin)
