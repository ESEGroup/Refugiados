#import bcrypt
from pymongo import MongoClient
from os import urandom
import binascii
from .utils import Utils
from .config import Config

class Status:
    NOT_RESOLVED = "Não resolvido"
    RESOLVED = "Resolvido"

class Models:
    class User:
        is_employee = False
        is_admin = False

        def __init__(self, CPF, name):
            self.CPF = Utils.clean_CPF(CPF)
            self.name = name

        def __str__(self):
            return self.name + " (" + self.CPF + ")"

    class Employee(User):
        is_employee = True

        def __init__(self, CPF, name, password):
            super().__init__(CPF, name)
            self.password = Models.Employee.__hash_pass(password)
            self.is_approved = is_approved

        def create(CPF="", name="", password="", is_admin=False, is_approved=False):
            return Models.Admin(CPF, name, password, is_admin, is_approved=is_approved) or \
                        Models.Employee(CPF, name, password, is_approved=is_approved)

        def __hash_pass(password):
            #if isinstance(password, str):
            #    password = bytes(password, 'utf-8')
            #password = bcrypt.hashpw(password, bcrypt.gensalt())
            return password

        def auth(user, password):
            if user and Models.Employee.__hash_pass(password) == user.password:
                return user
            return Models.User("","")

        def save(self):
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            result = db.users.insert_one(
                {
                    "CPF": self.CPF,
                    "name": self.name,
                    "is_admin": self.is_admin,
                    "is_approved": self.is_approved
                }
            )

        def update(self):
            pass

        def approve_user(self, user):
            return user

        def get_one(CPF):
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            user = db.user.find_one({'CPF':CPF})
            return user

    class Admin(Employee):
        is_admin = True

        def __init__(self, CPF, name, password, is_admin=True, is_approved=False):
            if not is_admin:
                return None
            super().__init__(CPF, name, password, is_approved=False)

        def approve_user(self, user):
            user.is_approved = True
            user.update()
            return user

        def __str__(self):
            return "Admin: " + super().__str__()

    class OccurrenceType:
        def __init__(self, name):
            self.name = name

        def get_all():
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            types = db.occurrence_types.find()

            return types

    class Occurrence:
        def __init__(self, user, date, occurrence, description, lat, lng, place_name, protocol_number=None):
            self.CPF = user.CPF
            self.name = user.name
            self.date = date
            self.occurrence = occurrence
            self.location = (lat, lng)
            self.place_name = place_name
            self.description = description
            self.status = Status.NOT_RESOLVED
            self.feedback_date = None
            self.feedback = None
            self.protocol_number = protocol_number or binascii.hexlify(urandom(5)).upper().decode('utf-8')

        def get_all():
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            occurrences = db.ocorrencias.find()
            return occurrences

        def get_one(CPF, protocol):
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            occurrence = db.ocorrencias.find_one({'CPF':CPF,'numeroProtocolo':protocol})
            return occurrence

        def save(self):
            client = mongoclient(str(config.mongodb))
            db = client.admin
            db.authenticate(config.mongodb.username, config.mongodb.password)
            db = client.projetox9
            result = db.ocorrencias.insert_one(
                {
                    "CPF" : self.CPF,
                    "nome" : self.name,
                    "data" : self.date,
                    "ocorrencia" : self.occurrence,
                    "localizacao": {
                        "latitude" : self.location[0],
                        "longitude" : self.location[1]
                    },
                    "nomeLugar" : self.place_name,
                    "descricao" : self.description,
                    "status" : self.status,
                    "dataFeedback" : self.feedback_date,
                    "feedback" : self.feedback,
                    "numeroProtocolo" : self.protocol_number
                }
            )

        def update(self):
            pass

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.lower() + " em " + self.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
