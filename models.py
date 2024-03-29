from peewee import *
from datetime import datetime

db = SqliteDatabase('database.db')

def cli_menu(options):
    for i, option in enumerate(options, start=1):
        print(f"{i} - {option}")
    while True:
        try:
            selection = int(input("Enter your choice: "))
            if 1 <= selection <= len(options):
                return options[selection - 1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(primary_key=True, unique=True)
    password = CharField(null=False)
    name = CharField(null=False)
    email = CharField(null=False, unique=True)

    @classmethod
    def login(cls, username: str, password: str) -> 'User' or None:
        try:
            user = cls.get(cls.username == username)
            if user.password == password:
                return user
        except:
            return None
    class Meta:
        database = db

class Clinic(BaseModel):
    id = CharField(primary_key=True)
    name = CharField(unique=True, null=False)
    email = CharField(unique=True, null=False)
    address = CharField(unique=True, null=False)
    services = CharField()
    is_available = BooleanField()

    @classmethod
    def get_clinics(cls):
        return [clinic for clinic in cls.select()]
    
    @classmethod
    def search_clinics(cls, query: str) -> list:
        query = query.lower()
        clinics = (cls
                .select()
                .where((fn.LOWER(cls.name).contains(query)) | 
                        (fn.LOWER(cls.services).contains(query)))
                .limit(5))
        return [clinic for clinic in clinics]
    class Meta:
        database = db

class Appointment(BaseModel):
    id = AutoField()
    status = CharField()
    date = DateTimeField(null=True)
    user = ForeignKeyField(User, backref='appointments')
    clinic = ForeignKeyField(Clinic, backref='appointments')

    def cancel_appointment(self):
        self.status = "CANCELLED"
        self.save()

    def accept_appointment(self, date):
        self.status = "ACTIVE"
        self.date = date
        self.save()
    class Meta:
        database = db

class Patient(BaseModel):
    user = ForeignKeyField(User, backref='patient')

    def get_pending_appointments(self):
        return [appointment for appointment in Appointment.select().where((Appointment.user == self.user) & (Appointment.status == 'PENDING'))]

    def get_active_appointments(self):
        return [appointment for appointment in Appointment.select().where((Appointment.user == self.user) & (Appointment.status == 'ACTIVE'))]

    def get_past_appointments(self):
        return [appointment for appointment in Appointment.select().where((Appointment.user == self.user) & (Appointment.status == 'PAST'))]

    def new_appointment(self, clinic):
        appointment = Appointment.create(status='PENDING', user=self.user, clinic=clinic)
        return appointment
    class Meta:
        database = db

class Monshi(BaseModel):
    user = ForeignKeyField(User, backref='monshi')
    clinic = ForeignKeyField(Clinic, backref='monshiha', null=True)

    def get_active_appointments(self):
        return [appointment for appointment in Appointment.select().where((Appointment.clinic == self.clinic) & (Appointment.status == 'ACTIVE'))]

    def get_pending_appointments(self):
        return [appointment for appointment in Appointment.select().where((Appointment.clinic == self.clinic) & (Appointment.status == 'PENDING'))]

    class Meta:
        database = db