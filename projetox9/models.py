import bcrypt
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from os import urandom
import binascii
from ..projetox9 import Config
from .utils import Utils

class Status:
    WAITING = "Aguardando resposta"
    ANSWERED = "Respondido"
    RESOLVED = "Resolvido"

class DB:
    def connect():
        client = MongoClient(str(Config.mongodb))
        db = client.admin
        db.authenticate(Config.mongodb.username, Config.mongodb.password)
        return client.ProjetoX9

class Models:
    class User:
        is_employee = False

        def __init__(self, CPF, name):
            self.CPF = CPF
            self.name = name or ""

        def __str__(self):
            return "{0} ({1})".format(
                            self.name,
                            self.CPF)

        def empty():
            return Models.User("","")

        def update(self):
            pass

        def create(CPF, name, is_employee, is_admin):
            if is_employee:
                return Models.Employee.create(CPF=CPF, name=name, is_admin=is_admin)
            else:
                return Models.User(CPF, name)

    class Employee(User):
        is_employee = True
        is_admin = False

        def __init__(self, CPF, name, password=None, pk=None, is_approved=False, hash=None):
            super().__init__(CPF, name)
            self.password = hash or Models.Employee.__hash_pass(password)
            self.is_approved = is_approved
            self.pk = pk

        def __str__(self):
            return "{0} - {1}aprovado".format(
                                            super().__str__(),
                                            "" if self.is_approved else "não ")

        def create(CPF="", name="", password="", is_admin=False, is_approved=False, pk=None, hash=None):
            if (is_admin):
                return Models.Admin(CPF, name, password=password, is_approved=is_approved, pk=pk, hash=hash)
            else:
                return Models.Employee(CPF, name, password=password, is_approved=is_approved, pk=pk, hash=hash)

        def __hash_pass(password):
            if password:
                if isinstance(password, str):
                    password = bytes(password, 'utf-8')

                return bcrypt.hashpw(password, bcrypt.gensalt())

        def __check_pass(password, hash):
            if password and hash:
                if isinstance(password, str):
                    password = bytes(password, 'utf-8')
                if isinstance(hash, str):
                    hash = bytes(hash, 'utf-8')

                return bcrypt.checkpw(password, hash)

        def to_dict(self):
            return {
                    "CPF": self.CPF,
                    "password": self.password,
                    "name": self.name,
                    "is_admin": self.is_admin,
                    "is_approved": self.is_approved}

        def from_dict(employee):
            if not employee: return None
            return Models.Employee.create(
                    pk=employee["_id"],
                    CPF=employee["CPF"],
                    name=employee["name"],
                    hash=employee["password"],
                    is_admin=employee["is_admin"],
                    is_approved=employee["is_approved"])

        def empty():
            return Models.Employee("","","")

        def approve_employee(self, employee):
            return employee

        def auth(employee, password):
            if Models.Employee.__check_pass(password, employee.password):
                return employee

            return Models.Employee.empty()

        def save(self):
            db = DB.connect()
            result = db.users.insert_one(self.to_dict())

        def update(self, set_dict):
            db = DB.connect()
            result = db.users.update_one({'CPF':self.CPF},{"$set":set_dict})

        def get_all(d):
            db = DB.connect()
            employees = db.users.find(d)

            return [Models.Employee.from_dict(e) for e in employees if e]

        def get_one(CPF, pk=None):
            db = DB.connect()
            d = {"CPF": CPF}
            if pk:
                d["_id"] = ObjectId(pk)
            employee = db.users.find_one(d)

            return Models.Employee.from_dict(employee)

        def get_one_or_empty(CPF, pk=None):
            return Models.Employee.get_one(CPF, pk) or Models.Employee.empty()

    class Admin(Employee):
        is_admin = True

        def approve_employee(self, employee):
            employee.update({"is_approved": True})
            return employee

        def __str__(self):
            return "Admin: " + super().__str__()

    class OccurrenceType:
        def __init__(self, pk, name):
            self.pk = pk
            self.name = name

        def to_dict(self):
            return {"_id":str(self.pk), "name":self.name}

        def from_dict(d):
            if not d: return None
            return Models.OccurrenceType(ObjectId(d["_id"]), d["name"])

        def empty():
            return Models.OccurrenceType("","")

        def get_one(pk):
            db = DB.connect()
            oc_type = db.occurrence_types.find_one({'_id': ObjectId(pk)})
            return Models.OccurrenceType.from_dict(oc_type)

        def get_one_or_empty(pk):
            return Models.OccurrenceType.get_one(pk) or Models.OccurrenceType.empty()

        def get_all():
            db = DB.connect()
            types = db.occurrence_types.find()

            return [Models.OccurrenceType.from_dict(t) for t in types if t]

        def __str__(self):
            return self.name + " (" + str(self.pk) + ")"

    class Location:
        def __init__(self, lat, lng, place_name):
            self.lat = lat
            self.lng = lng
            self.place_name = place_name

    class Occurrence:
        def __init__(self, CPF, name, date, occurrence, description, lat, lng, place_name, protocol_number=None, pk=None, status=None, feedback_date=None, feedback=None):
            self.pk = pk
            self.CPF = CPF
            self.name = name
            self.date = date
            self.occurrence = occurrence
            self.location = Models.Location(lat, lng, place_name)
            self.description = description
            self.status = status or Status.WAITING
            self.feedback_date = feedback_date
            self.feedback = feedback
            self.protocol_number = protocol_number or binascii.hexlify(urandom(5)).upper().decode('utf-8')

        def from_dict(d):
            if not d: return None
            return Models.Occurrence(
                    d["CPF"],
                    d["name"],
                    Utils.from_timestamp(d["date"]),
                    Models.OccurrenceType.from_dict(d["occurrence"]),
                    d["description"],
                    d["location"]["lat"],
                    d["location"]["lng"],
                    d["location"]["place_name"],
                    d["protocol_number"],
                    d["_id"],
                    d["status"],
                    d["feedback_date"],
                    d["feedback"])

        def to_dict(self):
            return {
                "CPF" : self.CPF,
                "name" : self.name,
                "date" : Utils.to_timestamp(self.date),
                "occurrence" : self.occurrence.to_dict(),
                "location": {
                    "lat" : self.location.lat,
                    "lng" : self.location.lng,
                    "place_name" : self.location.place_name,
                },
                "description" : self.description,
                "status" : self.status,
                "feedback_date" : self.feedback_date,
                "feedback" : self.feedback,
                "protocol_number" : self.protocol_number}

        def get_all():
            db = DB.connect()
            occurrences = db.occurrences.find().sort('date', DESCENDING).limit(Config.manager_N_last_occurrences)

            return [Models.Occurrence.from_dict(o) for o in occurrences if o]

        def get_one(CPF, protocol):
            db = DB.connect()
            occurrence = db.occurrences.find_one({'CPF':CPF,'protocol_number':protocol})

            return Models.Occurrence.from_dict(occurrence)

        def save(self):
            db = DB.connect()
            result = db.occurrences.insert_one(self.to_dict())

        def update(self):
            db = DB.connect()
            result = db.occurrences.update_one(
                            {'CPF':self.CPF,
                             'protocol_number':self.protocol_number},
                            {'$set': self.to_dict()})

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.name.lower() + " em " + self.location.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
