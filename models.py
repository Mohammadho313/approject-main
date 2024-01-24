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
    username = CharField(primary_key=True)
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