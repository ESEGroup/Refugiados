from config import Config
from api import Api

class testSaveOccurrence():
    api = Api()

    def __init__(self):
        testSaveOccurrence.api.set_occurrence("131.013.677-78", "Assalto", "14/11/2016 03:00:00", "Assalto no ponto do CT", "-22.858352", "-43.231569", "Ponto do CT")

testSaveOccurrence()
    
