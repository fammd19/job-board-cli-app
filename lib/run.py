from env import session, clear
from models import Job, Candidate, Company, Application
from sqlalchemy import func, and_
from colorama import Fore, Back, Style
import re

#once you've applied, not repspongin to no on no withdraw application - sorted?
#filtering by salay not working - sorted. Was showing less than min salary
#error handling on filters - sorted? Loop in wrong place
#application id is confusing in __repr__ - sorted> Updated defauult output for apllication and company 
#change job display to show only 10 at a time, then show next 10 as y/n
#once details are updated: show details
#when logging back in, show name of person logging in before clear - sorted?




logged_user = None

departments = ["Finance","Human Resources","Marketing","Operations","Sales","Technology"]
industries = ["Agriculture","Construction","Health & Education","Financial Services","Hopitality","Legal","Manufactuting","Retail","Technology"]
sizes = ["1-10","11-50","51-100","101-200","200-500","500+"]

def heading(text):
    print("*"*30)
    print(Fore.YELLOW + text.upper() +Style.RESET_ALL)
    print("*"*30)


def handle_yes_no(message):
    response = True

    while True:
        print(message)
        choice = input()

        if choice.lower() == "yes" or choice.lower() == "y":
            return True
        elif choice.lower() == "no" or choice.lower() == "n":
            return False
        else:
            print("Invalid input. Please select 'yes' or 'no'")


def main_menu():
    heading ("main menu")
    print("1. Jobs - view and filter open jobs")
    print("2. Applications - check your applications")
    print("3. Update - update your login details")
    print("4. Delete - delete account and exit")
    print("5. Logout")

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

    global logged_user
    logged_user = user


def check_email(email):
    regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    valid_email = re.match(regex, email)

    if not logged_user:
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
    
    if logged_user:
        if not valid_email:
            email_error = True
            while email_error:
                print("Please enter a valid email:")
                email=input()
                valid_email = re.match(regex, email)
                if valid_email:
                    return email
                    
        else:
            return email


def welcome():

    print("Welcome to the Job Board CLI App")
    print("Please enter your email address to login:")
    email = input()
    check_email(email)



def show_job_details(id):

    clear()

    loop = True

    while loop:
        job = session.query(Job).filter(Job.id==id).first()
        company = session.query(Company).join(Job, Company.id == Job.company_id).filter(Job.id==id).first()

        if job:
            heading("Job details")

            print(f"""
            {job.id}: {job.title}, {job.department}
            Date posted: {job.date_posted}
            Salary: {job.salary}
            Company: {company.name}
            Industry: {company.industry}
            Size: {company.size}
            """)

            apply(job, company)
            break

        else:
            print("Please select a valid job ID or press any key to go to the main menu")
            id = input()
    
def apply(job, company):
    choice = handle_yes_no("Would you like to apply for this job?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice:
        applications = session.query(Application).filter(Application.candidate_id==logged_user.id).all()
        if len(applications) <= 3:
            application = session.query(Application).filter(and_(Application.job_id==job.id, Application.candidate_id==logged_user.id)).first()
            if application:
                clear()
                print("You've already applied for this role. Here are your current applications:")
                show_applications()
            else:
                new_application = Application(job_id=job.id, candidate_id=logged_user.id)    
                session.add(new_application)
                session.commit()
                clear()
                print(f"Congratulations! You've successfully applied to {job.title} at {company.name}")
                show_applications()

        else:
            clear()
            print("You've applied for the maximum number of jobs. Here are your existing applications:")
            show_applications()

def filter_jobs():
    print("""Filter by:
            1. Industry
            2. Company size
            3. Department
            4. Salary
            Please select an option""")

    loop = True

    while loop:
        choice = input()

        if choice.lower() == "industry" or choice == "1":
            clear()
            for industry in industries:
                print(industry)
            print("Please select an industry")
            choice = input()
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(func.lower(Company.industry) == choice)
            for job in jobs:
                print(job)
            print("Select an id to show the jobs details, or press any key to go the main menu")
            choice = input()
            if choice.isdigit():
                job_id = int(choice)
                show_job_details(job_id)
            break

        elif choice.lower() == "company size" or choice.lower() == "company" or choice.lower() == "size" or choice == "2":
            clear()
            for size in sizes:
                print(size)
            print("Please select a company size")
            choice = input()
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(Company.size == choice)
            for job in jobs:
                print(job)
            print("Select an id to show the jobs details, or press any key to go the main menu")
            choice = input()
            if choice.isdigit():
                job_id = int(choice)
                show_job_details(job_id)
            break

        elif choice.lower() == "department" or choice == "3":
            clear()

            for department in departments:
                print(department)
            print("Please select a department")

            choice = input()
            jobs = session.query(Job).filter(func.lower(Job.department) == choice.lower()).all()

            if len(jobs)>0:
                for job in jobs:
                    print(job)
                print("Select an id to show the jobs details, or press any key to go the main menu")
                choice = input()
                if choice.isdigit():
                    job_id = int(choice)
                    show_job_details(job_id)
            
            else:
                print(f"There are no jobs currently available in {choice}")
                view_all_jobs()

        elif choice.lower() == "salary" or choice == "4":
            print("Please enter a minimum salary:")
            min_sal = input()
            jobs = session.query(Job).filter(Job.salary>=min_sal).all()
            for job in jobs:
                print(job)
            print("Select an id to show the jobs details, or press any key to go the main menu")
            choice = input()
            if choice.isdigit():
                job_id = int(choice)
                show_job_details(job_id)
            break

        else:
            print("Invalid input. Please select again:")


def view_all_jobs():
    jobs = session.query(Job).all()
    heading("Open jobs")
    for job in jobs:
        print(job)

    print("\nWhat would you like to do next?")

    while True:
        print("View a job - please enter the ID of the job you'd like to view")
        print("Filter jobs - select 'filter'")
        print("Menu - back to the main menu")
        choice = input()

        if choice.isdigit():
            job_id = int(choice)
            show_job_details(job_id)
            break
        elif choice.lower() == "filter":
            filter_jobs()
            break
        elif choice.lower() == "menu":
            break
        else:
            print("Please select a valid option")

def withdraw (id):
    app_to_delete = session.query(Application).filter(Application.id==id).first()
    session.delete(app_to_delete)
    session.commit()


def show_applications():
    clear()
    loop = True
    while loop:
        applications = session.query(Application).filter(Application.candidate_id==logged_user.id).all()
        if len(applications)>0:
            heading("Current applications")
            for application in applications:
                company = session.query(Company).filter(Company.id == application.job.company_id).first()
                print(f"{application} | {company}")
            choice = handle_yes_no("Would you like to withdraw any applications?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
            if choice:
                print(Fore.RED+"Please enter the ID to withdraw:"+Style.RESET_ALL)
                id = input()
                withdraw(id)
            else:
                loop = False
        else:
            print("You have not applied to any jobs yet\n")
            choice = handle_yes_no("Would you like to view open jobs?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
            if choice:
                view_all_jobs()
            break



def update_details():
    user_to_update = session.query(Candidate).filter(Candidate.id==logged_user.id).first()
    choice = handle_yes_no("Update name?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice: 
        print("Enter updated name:")
        name=input()
        user_to_update.full_name = name
        logged_user.full_name = name
        session.commit()
    choice = handle_yes_no("Update email?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice:
        print("Enter updated email:")
        email=input()
        valid_email = check_email(email)
        user_to_update.email = valid_email
        logged_user.email = valid_email
        session.commit()
    print(f"{logged_user.full_name} - {logged_user.email}")
    print("Press enter to go back to the main menu")
    input()

def delete_profile():
    global logged_user
    print("Deleting your profile will remove any open applications and log you out")

    choice = handle_yes_no(Fore.RED+"Are you sure you want to delete your profile?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice:
        user_to_delete = session.query(Candidate).filter(Candidate.id==logged_user.id).first()
        session.delete(user_to_delete)
        session.commit()
        print("Account successfully deleted")
        logged_user = None

def candidate_details():
    print(f"Name: {logged_user.full_name}\nEmail: {logged_user.email}")
    choice = handle_yes_no("Do you want to update your details?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice:
        update_details()
    choice = handle_yes_no("Do you want to delete your account?"+Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
    if choice:
        delete_profile()

def start():
    welcome()
    loop = True

    global logged_user
    if logged_user:

        while loop:
            if logged_user == None:
                loop = False
            else:
                choice = main_menu()
                while True:
                    if choice.lower() == "jobs" or choice == "1":
                        view_all_jobs()
                        break
                    elif choice.lower() == "applications" or choice == "2":
                        clear()
                        show_applications()
                        break
                    elif choice.lower() == "update" or choice == "3":
                        clear()
                        candidate_details()
                        break
                    elif choice.lower() == "delete" or choice == "4":
                        clear()
                        delete_profile()
                        break
                    elif choice.lower() == "logout" or choice.lower() == "quit" or choice.lower() == "exit" or choice == "5":
                        clear()
                        loop = False
                        break
                    else:
                        print("Invalid input. Please select again:")
                        choice = input()
    print("Thanks for using the Job Board CLI App!")


if __name__ == "__main__":
    start()