#import bcrypt
from os import urandom
import binascii

class Status:
    NOT_RESOLVED = 0
    RESOLVED = 1

class Models:
    class User:
        is_employee = False
        is_admin = False

        def __init__(self, CPF, name):
            self.CPF = CPF.replace(".","").replace("-","-")
            self.name = name

        def __str__(self):
            return self.name + " (" + self.CPF + ")"

    class Employee(User):
        is_employee = True

        def __init__(self, CPF, name, password):
            super().__init__(CPF, name)

            if isinstance(password, str):
                password = bytes(password, 'utf-8')
            self.password = password #bcrypt.hashpw(password, bcrypt.gensalt())

    class Admin(Employee):
        is_admin = True

        def __str__(self):
            return "Admin: " + super().__str__()

    class Occurrence:
        def __init__(self, user, date, occurrence, description, lat, lng, place_name):
            self.CPF = user.CPF
            self.name = user.name
            self.date = date
            self.occurrence = occurrence
            self.local = (lat, lng)
            self.place_name = place_name
            self.description = description
            self.status = Status.NOT_RESOLVED
            self.feedback_date = None
            self.feedback = None
            self.protocol_number = str(binascii.hexlify(urandom(5)).upper())

        def __str__(self):
            return "[" + self.protocol_number + "] " + str(self.name) + " reportou " + self.occurrence.lower() + " em " + self.place_name + " às " + self.date.split(" ")[1] + " de " + self.date.split(" ")[0]
