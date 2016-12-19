import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from ..projetox9 import Config
from .models import Models, Status
from .utils import Utils

class Api:
    models = Models()

    def get_occurrence_types(self):
        return self.models.OccurrenceType.get_all()

    def get_occurrence_type(self, pk):
        return self.models.OccurrenceType.get_one_or_empty(pk)

    def get_occurrences(self):
        return self.models.Occurrence.get_all()

    def get_occurrence(self, CPF, protocol):
        return self.models.Occurrence.get_one(Utils.clean_CPF(CPF), protocol.upper())

    def get_employees_not_approved(self, admin):
        if not admin: return
        return self.models.Employee.get_all({"is_approved":False})

    def set_occurrence(self, CPF, name, oc_type_pk, date, description, lat, lng, place_name):
        user = self.get_person_info(Utils.clean_CPF(CPF))
        occurrence_type = self.get_occurrence_type(oc_type_pk)
        
        if user.name == "" or " ":
            oc = self.models.Occurrence(user.CPF, name, date, occurrence_type, description, lat, lng, place_name) 
        else:
            oc = self.models.Occurrence(user.CPF, user.name, date, occurrence_type, description, lat, lng, place_name)
        
        oc.save()
        return oc

    def update_occurrence(self, CPF, protocol, status, feedback_date, feedback):
        occurrence = self.models.Occurrence.get_one(CPF, protocol)
        if occurrence:
            occurrence.status = status
            occurrence.feedback_date = feedback_date
            occurrence.feedback = feedback
            occurrence.update()

    def login(self, CPF, password):
        employee = self.models.Employee.get_one_or_empty(Utils.clean_CPF(CPF))
        employee = self.models.Employee.auth(employee, password)

        logged = employee.is_approved
        admin = logged and employee.is_admin

        return logged, admin

    def signup(self, CPF, password, admin):
        employee = self.get_person_info(Utils.clean_CPF(CPF))
        employee = self.models.Employee.create(CPF=employee.CPF, name=employee.name, is_admin=employee.is_employee and employee.is_admin, password=password)
        employee.save()

        if employee.name != "":
            return self.approve_employee(admin, employee.CPF, employee=employee)
        else:
            return employee

    def approve_employee(self, admin, CPF, pk=None, name=None, employee=None):
        employee = employee or self.models.Employee.get_one_or_empty(CPF, pk=pk)
        if name and name != "":
            employee.update({"name": name})

        manager = self.models.Employee.create(is_admin=admin, is_approved=admin)
        return manager.approve_employee(employee)

    def get_status_list(self):
        return [getattr(Status,s) for s in Status.__dict__ if not s.startswith("__")]

    # FakeSiga
    def get_person_info(self, CPF):
        base_url = str(Config.FakeSiga)
        path = '/api/Dados/findOne?filter={"where":{"CPF":"' + CPF + '"}}'

        data = {}
        try:
            f = urlopen(base_url + path)
            data = json.loads(f.read().decode('utf-8'))
        except URLError as e:
            pass

        is_admin = data.get("FuncionarioAdministrativo") or False
        is_employee = data.get("Professor") or data.get("ProfessorVisitante") or data.get("FuncionarioTerceirizado") or is_admin

        return self.models.User.create(data.get("CPF",CPF), data.get("Nome",""), is_employee, is_admin)
