from env import session, clear
from models import Job, Candidate, Company, Application
import re

def heading(text):
    print("*"*30)
    print(text.upper())
    print("*"*30)


def handle_yes_no(message):
    response = True

    while True:
        print(message)
        choice = input()

        if choice.lower() == "yes" or choice.lower() == "y":
            response = True
            break
        elif choice.lower() == "no" or choice.lower() == "n":
            response = False
            break
        else:
            print("Invalid input. Please select 'yes' or 'no'")


def main_menu():
    heading ("main menu")
    print("1. Jobs - view and filter open jobs")
    print("1. Applications - check your applications")
    print("3. Update - update your login details")
    print("4. Logout")

    print("Please enter your choice:")

    return input()


def login(email):
    user = session.query(Candidate).filter(Candidate.email == email).first()

    entry_error = False

    if not user:
        print("\nPlease enter your full name:")
        print("If you've registered before, please type 'back' and re-enter your email")
        name = input()

        if name == "back":
            entry_error = True
            while entry_error:
                clear()
                print("Let's try again. Please enter your email:")
                print("Enter new to regsiter as a new user")
                email = input()
                if email == "new":
                    clear()
                    entry_error = False
                    print("Please enter the email you'd like to register with:")
                    email = input()
                    check_email(email)

                else: 
                    user = session.query(Candidate).filter(Candidate.email == email).first()
                    if user:
                        entry_error=False 
                        print(f"We've found you now! Welcome back {user.full_name}")
                    else:
                        print("We still haven't found your details.")
                        entry_error=True 

        else:
            user = Candidate(email = email, full_name = name)
            session.add(user)
            session.commit()

            print("You have successfully registered.")
                    
    else:
        print(f"Welcome back {user.full_name}")


def check_email(email):
    regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    valid_email = re.match(regex, email)

    if not valid_email:
        email_error = True
        while email_error:
            print("Please enter a valid email:")
            email=input()
            valid_email = re.match(regex, email)
            if valid_email:
                email_error = False
                login(email)

    else:
        login(email)




def welcome():

    print("Welcome to the Job Board CLI App")
    print("Please enter your email address to login:")
    email = input()
    check_email(email)



def show_job_details():
    pass


def apply():
    pass


def view_all_jobs():
    jobs = session.query(Job).all()
    for job in jobs:
        print (job)


def filter_jobs(filter):
    pass


def check_applications():
    pass


def update_details():
    pass


def delete_profile():
    pass


def candidate_details():
    pass


def start():
    welcome()
    loop = True

    while loop:
        choice = main_menu()
        while True:
            if choice.lower() == "jobs":
                view_all_jobs()
                break
            elif choice.lower() == "applications":
                pass
            elif choice.lower() == "update":
                pass
            elif choice.lower() == "logout" or choice.lower() == "quit" or choice.lower() == "exit":
                loop = False
                break
            
            else:
                print("Invalid input. Please select again:")

    print("Thanks for using the Job Board CLI App!")


if __name__ == "__main__":
    start()