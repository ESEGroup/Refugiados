#import bcrypt
from os import urandom
import binascii

class Status:
    NOT_RESOLVED = "Não resolvido"
    RESOLVED = "Resolvido"

class Models:
    class User:
        is_employee = False
        is_admin = False

        def __init__(self, CPF, name, is_employee):
            self.CPF = CPF.replace(".","").replace("-","-")
            self.name = name

        def __str__(self):
            return self.name + " (" + self.CPF + ")"

    class Employee(User):
        is_employee = True

        def __init__(self, CPF, name, password, approved):
            super().__init__(CPF, name)

            self.approved = approved
            if isinstance(password, str):
                password = bytes(password, 'utf-8')
            self.password = password #bcrypt.hashpw(password, bcrypt.gensalt())

    class Admin(Employee):
        is_admin = True

        def __str__(self):
            return "Admin: " + super().__str__()

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

        def save(self):
            pass

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.lower() + " em " + self.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
