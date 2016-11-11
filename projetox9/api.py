from .models import Models
from projetox9 import config
class Api:
    def __init__(self):
        self.models = Models()

    def get_info_person(self, CPF):
        pass

    def create_occurrence(self, CPF, occurrence, date, description):
        print(CPF, occurrence, date, description)
