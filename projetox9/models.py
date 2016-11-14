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

        def __init__(self, CPF, name, password, pk=None, is_approved=False):
            super().__init__(CPF, name)
            self.password = Models.Employee.__hash_pass(password)
            self.is_approved = is_approved
            self.pk = None

        def create(CPF="", name="", password="", is_admin=False, is_approved=False, pk=None):
            if (is_admin):
                return Models.Admin(CPF, name, password, is_approved=is_approved, pk=pk)
            else:
                return Models.Employee(CPF, name, password, is_approved=is_approved, pk=pk)

        def __hash_pass(password):
            #if isinstance(password, str):
            #    password = bytes(password, 'utf-8')
            #password = bcrypt.hashpw(password, bcrypt.gensalt())
            return password

        @property
        def empty():
            return Models.Employee("","","")

        def auth(user, password):
            if user and Models.Employee.__hash_pass(password) == user.password:
                return user
            return Models.Employee.empty

        def save(self):
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            result = db.users.insert_one(
                {
                    "CPF": self.CPF,
                    "password": self.password,
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
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            user = db.users.find_one({'CPF':CPF})
            if user:
                return Models.Employee.create(CPF=user["CPF"], password=user["password"], is_admin=user["is_admin"], is_approved=user["is_approved"], pk=user["_id"])
            return Models.Employee.empty

    class Admin(Employee):
        is_admin = True

        def approve_user(self, user):
            user.is_approved = True
            user.update()
            return user

        def __str__(self):
            return "Admin: " + super().__str__()

    class OccurrenceType:
        def __init__(self, pk, name):
            self.pk = pk
            self.name = name

        def get_all():
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            types = db.occurrence_types.find({})

            ret = []
            for t in types:
                ret += [Models.OccurrenceType(t["_id"], t["name"])]

            return ret

        def __str__(self):
            return self.name + " (" + self.pk + ")"

    class Occurrence:
        def __init__(self, pk, user, date, occurrence, description, lat, lng, place_name, protocol_number=None):
            self.pk = pk
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
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            occurrences = db.ocorrencias.find()

            ret = []
            for t in occurrences:
                ret += [Models.Occurrence(t["_id"], Models.User(t["CPF"], t["name"]), t["date"], t["occurrence"], t["location"]["lat"], t["location"]["lng"], t["place_name"], t["protocol_number"])]
            return occurrences

        def get_one(CPF, protocol):
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            occurrence = db.occurrences.find_one({'CPF':CPF,'protocol_number':protocol})

            return Models.Occurrence(t["_id"], Models.User(t["CPF"], t["name"]), t["date"], t["occurrence"], t["location"]["lat"], t["location"]["lng"], t["place_name"], t["protocol_number"])

        def save(self):
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            result = db.ocurrences.insert_one(
                {
                    "CPF" : self.CPF,
                    "name" : self.name,
                    "date" : self.date,
                    "ocurrence" : self.occurrence,
                    "location": {
                        "lat" : self.location[0],
                        "lng" : self.location[1]
                    },
                    "place_name" : self.place_name,
                    "description" : self.description,
                    "status" : self.status,
                    "feedback_date" : self.feedback_date,
                    "feedback" : self.feedback,
                    "protocol_number" : self.protocol_number
                }
            )

        def update(self):
            pass

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.lower() + " em " + self.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
