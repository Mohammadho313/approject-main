from models import *
import random

db.connect()
db.create_tables([User, Clinic, Appointment, Patient, Monshi])

# Code to Create Clinics for testing
# clin = Clinic.create(id="2",name="clinic2", email="clinic2@clinic.com", address="address2", services="dandan sarma garma", is_available=True)
# clin.save()


def patient_main_menu(patient):
    while True:
        print("Welcome Patient!")
        print("Lotfan entekhab konid:")
        options = ["create appointment", "view pending appointments", "view ongoing appointments", "view past appointments", "update profile","logout"]
        opt = cli_menu(options)
        match opt:
            case "create appointment":
                create_new_appointment(patient)
            case "view pending appointments":
                view_pending_appointments(patient)
            case "view ongoing appointments":
                view_ongoing_appointments(patient)
            case "view past appointments":
                view_past_appointments(patient)
            case "update profile":
                update_user_profile(patient.user)
            case "logout":
                logout()
def update_user_profile(user):
    new_name = input("Enter your new name: ")
    new_email = input("Enter your new email: ")
    new_password = input("Enter your new pasword: ")
    user.name = new_name
    user.email = new_email
    user.password = new_password
    user.save()

def create_new_appointment(patient):
    while True:
        query = input("Search:")
        clinics = Clinic.search_clinics(query)
        inp = cli_menu([f"{clinic.name}" for clinic in clinics])
        clinic = Clinic.select().where(Clinic.name == inp).first()
        patient.new_appointment(clinic)
        print("Appointment created.")
        break


def view_pending_appointments(patient):
    appointments = patient.get_pending_appointments()
    while True:
        match cli_menu([f"{appointment.clinic.name}" for appointment in appointments]):
            case x:
                for appoint in appointments:
                    if appoint.clinic.name == x:
                        appoint.cancel_appointment()


def view_ongoing_appointments(patient):
    appointments = patient.get_active_appointments()
    while True:
        match cli_menu([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments]):
            case x:
                for appoint in appointments:
                    if appoint.clinic.name == x:
                        appoint.cancel_appointment()

def view_past_appointments(patient):
    appointments = patient.get_past_appointments()
    cli_menu([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments])


def monshi_main_menu(monshi):
    while True:
        match cli_menu(["pending appointments", "current appointments", "update profile", "logout"]):
            case "pending appointments":
                monshi_view_pending_appointments(monshi)
            case "current appointments":
                monshi_view_active_appointments(monshi)
            case "update profile":
                update_user_profile(monshi.user)
            case "logout":
                logout()


def monshi_view_active_appointments(monshi):
    apps = monshi.get_active_appointments()
    while True:
        match cli_menu([f"{appointment.user.name}" for appointment in apps]):
            case x:
                apps[x].cancel_appointment()


def monshi_view_pending_appointments(monshi):
    while True:
        appointments = monshi.get_pending_appointments()
        match cli_menu([f"{appointment.user.name}" for appointment in appointments]):
            case x:
                match cli_menu(["approve", "cancel"]):
                    case "approve":
                        for appoint in appointments:
                            if appoint.user.name == x:
                                while True:
                                    date = input("Date (YYYY/MM/DD HH:MM): ")
                                    try:
                                        dt = datetime.strptime(date, "%Y/%m/%d %H:%M")
                                        appoint.accept_appointment(dt)
                                        break
                                    except ValueError:
                                        print("Date error")
                    case "cancel":
                        appointments[x].cancel_appointment()
                        
def logout():
    print("Khooda Negahdar...! \n \n\n\n\n\n\n")
    main()


def main():
    print("Khosh Amadid!")
    while True:
        action = input("Do you want to 1-signup or 2-signin?»")

        if action.lower() == "1":
            username = input("Enter username for signup: ")
            name = input("Enter name for signup: ")
            email = input("Enter email for signup: ")
            password = input("Enter password for signup: ")
            try:
                user = User.create(username=username, password=password, name=name, email=email)
                user.save()
            except:
                print("Username or email already exists.")
                break
            role = input("Enter your role (1-monshi or 2-patient): ")
            if role.lower() == "1":
                clinic = Clinic.select().where(Clinic.id == input("Please enter clinic id: ")).first()
                monshi = Monshi.create(user=user,clinic=clinic)
                monshi.save()
                monshi_main_menu(patient)

            elif role.lower() == "2":
                patient = Patient.create(user=user)
                patient.save()
                patient_main_menu(patient)

            print("Signup Successful!")
            break

        elif action.lower() == "2":
            if(input("How you wanna login?(otp/pass): ") == "otp"):
                email = input("Enter your email address: ")
                user = User.select().where(User.email == email).first()
                if user is None:
                    print("Wrong email")
                    continue
                otp = random.randint(1000,9999)
                print("Please enter the otp code: ")
                print("TEMPORARY OTP: "+str(otp))
                if(input("OTP: ") == str(otp)):
                    print("Welcome!")
                else:
                    print("WRONG OTP")
                    continue
            else:
                username = input("Enter username for signin: ")
                password = input("Enter password for signin: ")
                user = User.login(username, password)
            if user is not None:
                print("Login Successful!")
                patient = Patient.select().where(Patient.user == user).first()
                if patient is not None:
                    print("Patient")
                    patient_main_menu(patient)
                else:
                    monshi = Monshi.select().where(Monshi.user == user).first()
                    if monshi is not None:
                        print("Monshi")
                        monshi_main_menu(monshi)
                break

main()