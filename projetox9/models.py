class Models:
    class BaseUser:
        def __init__(self, CPF, name):
            self.CPF = CPF
            self.name = name

        def __str__(self):
            return self.name + " (" + self.CPF + ")"

    class Employee(BaseUser):
        def __init__(self, CPF, name):
            super().__init__(CPF, name)

        def __str__(self):
            return "Employee: " + super().__str__()

    class Admin(BaseUser):
        def __init__(self, CPF, name):
            super().__init__(CPF, name)

        def __str__(self):
            return "Admin: " + super().__str__()

    class User:
        def __init__(self, CPF, name):
            super().__init__(CPF, name)

    class Occurrence:
        def __init__(self, CPF, name, date, occurrence, description, lat, lon):
            self.CPF = CPF
            self.name = name
            self.date = date
            self.occurrence = occurrence
            self.local = (lat, lon)
            self.description = description
