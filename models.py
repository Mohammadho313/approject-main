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
