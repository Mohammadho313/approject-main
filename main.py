from models import *


db.connect()
db.create_tables([User, Clinic, Appointment, Patient, Monshi])


def patient_main_menu():
    while True:
        print("Welcome Patient!")
        print("Lotfan entekhab konid:")
        options = ["create appointment", "view pending appointments", "view ongoing appointments", "view past appointments"]
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


def create_new_appointment(patient):
    while True:
        query = input("Search:")
        clinics = Clinic.search_clinics(query)
        inp = cli_menu([f"{clinic.name}:{clinic.services}" for clinic in clinics])
        patient.new_appointment(clinics[inp])
        print("Appointment created.")
        break


def view_pending_appointments(patient):
    appointments = patient.get_pending_appointments()
    while True:
        match cli_menu([f"{appointment.clinic.name}" for appointment in appointments]):
            case x:
                appointments[x].cancel_appointment()


def view_ongoing_appointments(patient):
    appointments = patient.get_active_appointments()
    while True:
        match cli_menu([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments]):
            case x:
                appointments[x].cancel_appointment()


def view_past_appointments(patient):
    appointments = patient.get_past_appointments()
    cli_menu([f"{appointment.clinic.name}: {appointment.date}" for appointment in appointments])


def monshi_main_menu(monshi):
    while True:
        match cli_menu(["pending appointments", "current appointments"]):
            case "pending appointments":
                monshi_view_pending_appointments(monshi)
            case "current appointments":
                monshi_view_active_appointments(monshi)


def monshi_view_active_appointments(monshi):
    apps = monshi.get_pending_appointments()
    while True:
        match cli_menu([f"{appointment.user.name}" for appointment in apps]):
            case x:
                apps[x].cancel_appointment()


def monshi_view_pending_appointments(monshi):
    appointments = monshi.get_active_appointments()
    while True:
        match cli_menu([f"{appointment.user.name}" for appointment in appointments]):
            case x:
                match cli_menu(["approve", "cancel"]):
                    case "approve":
                        break
                    case "cancel":
                        while True:
                            date = input("Date (YYYY/MM/DD HH:MM): ")
                            try:
                                dt = datetime.strptime(date, "%Y/%m/%d %H:%M")
                                appointments[x].accept_appointment(dt)
                                break
                            except ValueError:
                                print("Date error")

                    case 1:
                        appointments[x].cancel_appointment()



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
                patient_main_menu()
            if user.monshi != None:
                print("Monshi")
                monshi_main_menu()
            break
        else:
            print("Wrong Creds")
main()