from models import *


db.connect()
db.create_tables([User, Clinic, Appointment, Patient, Monshi])


def main():
    print("Khosh Amadid!")
    while True:
        username = input("Username»")
        password = input("Password»")

        user = User.login(username, password)
        if (user != None):
            print("Login Successful!")
            if user.patient != None:
                print("Patient")
            if user.monshi != None:
                print("Monshi")
            break
        else:
            print("Wrong Creds")
main()