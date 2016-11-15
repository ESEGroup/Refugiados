import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from os import urandom
import binascii
from projetox9 import Config

class Status:
    NOT_RESOLVED = "Não resolvido"
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
        is_admin = False

        def __init__(self, CPF, name=""):
            self.CPF = CPF
            self.name = name

        def __str__(self):
            return self.name + " (" + self.CPF + ")"

        def empty():
            return Models.User("","")

        def create(CPF, name, is_employee, is_admin):
            if is_employee:
                return Models.Employee.create(CPF=CPF, name=name, is_admin=is_admin)
            else:
                return Models.User(CPF, name)

    class Employee(User):
        is_employee = True

        def __init__(self, CPF, name, password=None, pk=None, is_approved=False, hash=None):
            super().__init__(CPF, name)
            self.password = hash or Models.Employee.__hash_pass(password)
            self.is_approved = is_approved
            self.pk = pk

        def create(CPF="", name="", password="", is_admin=False, is_approved=False, pk=None, hash=None):
            if (is_admin):
                return Models.Admin(CPF, name, password, is_approved=is_approved, pk=pk, hash=hash)
            else:
                return Models.Employee(CPF, name, password, is_approved=is_approved, pk=pk)

        def __hash_pass(password):
            if password:
                if isinstance(password, str):
                    password = bytes(password, 'utf-8')
                return bcrypt.hashpw(password, bcrypt.gensalt())

        def __check_pass(password, hash):
            if password and hash:
                if isinstance(password, str):
                    password = bytes(password, 'utf-8')
                return bcrypt.checkpw(password, hash)


        def empty():
            return Models.Employee("","")

        def auth(user, password):
            if Models.Employee.__check_pass(password, user.password):
                return user
            return Models.User.empty()

        def save(self):
            db = DB.connect()
            result = db.users.insert_one({
                        "CPF": self.CPF,
                        "password": self.password,
                        "name": self.name,
                        "is_admin": self.is_admin,
                        "is_approved": self.is_approved})

        def update(self):
            client = MongoClient(str(Config.mongodb))
            db = client.admin
            db.authenticate(Config.mongodb.username, Config.mongodb.password)
            db = client.ProjetoX9
            result = db.users.update_one({'CPF':self.CPF},{"is_admin": self.is_admin, "is_approved": self.is_approved})

        def approve_user(self, user):
            pass

        def get_one(CPF):
            db = DB.connect()
            user = db.users.find_one({'CPF':CPF})
            if user:
                return Models.Employee.create(
                        CPF=user["CPF"],
                        hash=user["password"],
                        is_admin=user["is_admin"],
                        is_approved=user["is_approved"],
                        pk=user["_id"])

        def get_one_or_empty(CPF):
            return Models.Employee.get_one(CPF) or Models.User.empty()

    class Admin(Employee):
        is_admin = True

        def approve_user(self, user):
            user.is_approved = True
            user.update()

        def __str__(self):
            return "Admin: " + super().__str__()

    class OccurrenceType:
        def __init__(self, pk, name):
            self.pk = pk
            self.name = name

        def to_dict(self):
            return {"_id":self.pk, "name":self.name}

        def from_dict(d):
            return Models.OccurrenceType(d["_id"], d["name"])

        def get_one(pk):
            db = DB.connect()
            oc_type = db.occurrence_types.find_one({'_id': ObjectId(pk)})

            if oc_type:
                return Models.OccurrenceType.from_dict(oc_type)

        def empty():
            return Models.OccurrenceType("","")

        def get_one_or_empty(pk):
            return Models.OccurrenceType.get_one(pk) or Models.OccurrenceType.empty()

        def get_all():
            db = DB.connect()
            types = db.occurrence_types.find()

            ret = []
            for t in types:
                ret += [Models.OccurrenceType.from_dict(t)]

            return ret

        def __str__(self):
            return self.name + " (" + str(self.pk) + ")"

    class Occurrence:
        def __init__(self, CPF, name, date, occurrence, description, lat, lng, place_name, protocol_number=None, pk=None):
            self.pk = pk
            self.CPF = CPF
            self.name = name
            self.date = date
            self.occurrence = occurrence
            self.location = (lat, lng)
            self.place_name = place_name
            self.description = description
            self.status = Status.NOT_RESOLVED
            self.feedback_date = None
            self.feedback = None
            self.protocol_number = protocol_number or binascii.hexlify(urandom(5)).upper().decode('utf-8')

        def from_dict(d):
            if not d: return None
            return Models.Occurrence(
                    d["CPF"],
                    d["name"],
                    d["date"],
                    Models.OccurrenceType.from_dict(d["occurrence"]),
                    d["description"],
                    d["location"]["lat"],
                    d["location"]["lng"],
                    d["place_name"],
                    d["protocol_number"],
                    d["_id"])

        def to_dict(self):
            return {
                "CPF" : self.CPF,
                "name" : self.name,
                "date" : self.date,
                "occurrence" : self.occurrence.to_dict(),
                "location": {
                    "lat" : self.location[0],
                    "lng" : self.location[1]
                },
                "place_name" : self.place_name,
                "description" : self.description,
                "status" : self.status,
                "feedback_date" : self.feedback_date,
                "feedback" : self.feedback,
                "protocol_number" : self.protocol_number}

        def get_all():
            db = DB.connect()
            occurrences = db.occurences.find()

            ret = []
            for o in occurrences:
                ret += Models.Occurrence.from_dict(o)

            return ret

        def get_one(CPF, protocol):
            db = DB.connect()
            occurrence = db.occurrences.find_one({'CPF':CPF,'protocol_number':protocol})
            return Models.Occurrence.from_dict(occurrence)

        def save(self):
            db = DB.connect()
            result = db.occurrences.insert_one(self.to_dict())
            return result

        def update(self):
            pass

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.name.lower() + " em " + self.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
