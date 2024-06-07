from env import session, clear
from models import Job, Candidate, Company, Application
from sqlalchemy import func, and_
from colorama import Fore, Back, Style
import re

logged_user = None

departments = [(1,"Finance"), (2,"Human Resources"), (3,"Marketing"),(4,"Operations"),(5,"Sales"),(6,"Technology")]
industries = [(1,"Agriculture"), (2,"Construction"),(3,"Health & Education"),(4,"Financial Services"),(5,"Hospitality"),(6,"Legal"),(7,"Manufactuting"),(8,"Retail"),(9,"Technology")]
sizes = [(1,"1-10"),(2,"11-50"),(3,"51-100"),(4,"101-200"),(5,"200-500"),(6,"500+")]

def heading(text):
    print("*"*30)
    print(Fore.YELLOW + text.upper() +Style.RESET_ALL)
    print("*"*30)


def subheading(text):
    print(Fore.CYAN + text.upper() +Style.RESET_ALL)


def handle_yes_no(message):
    response = True

    while True:
        print(f"{message}" +Style.BRIGHT+" (y/n)"+Style.RESET_ALL)
        choice = input()

        if choice.lower() == "yes" or choice.lower() == "y":
            return True
        elif choice.lower() == "no" or choice.lower() == "n":
            return False
        else:
            print("Invalid input. Please select 'yes' or 'no'")


def main_menu():
    heading("main menu")
    print("1. All Jobs - view all open jobs")
    print("2. Filter - filter jobs by department, industry, company size or salary")
    print("3. Applications - check your applications")
    print("4. Account - update your login details or delete your account")
    print("5. Logout")

    print("Please enter your choice:")

    return input()


def login(email):
    user = session.query(Candidate).filter(Candidate.email == email).first()

    entry_error = False

    if not user:
        loop = True
        while loop:
            print("\nPlease enter your full name:")
            print("If you've registered before, please type 'back' and re-enter your email")
            name = input()

            if name == "back":
                entry_error = True
                while entry_error:
                    print("Let's try again. Please enter your email:")
                    print("Enter new to regsiter as a new user")
                    email = input()
                    if email == "new":
                        entry_error = False
                        print("Please enter the email you'd like to register with:")
                        email = input()
                        check_email(email)

                    else: 
                        user = session.query(Candidate).filter(Candidate.email == email).first()
                        if user:
                            entry_error=False 
                            print(f"We've found you now! Welcome back {user.full_name}")
                            break
                        else:
                            print("We still haven't found your details.")
                            entry_error=True 

            elif name:
                user = Candidate(email = email, full_name = name)
                session.add(user)
                session.commit()
                clear()
                print(f"Welcome {user.full_name}.You have successfully registered. What would you like to do first?")
                break

            else:
                clear()
                print("Name cannot be blank.")
                    
    else:
        clear()
        print(f"Welcome back {user.full_name}. What would you like to do?")

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

    subheading("Welcome to the Job Board CLI App")
    print("Please enter your email address to login:")
    email = input()
    check_email(email)


def show_job_details(id):

    loop = True

    while loop:
        job = session.query(Job).filter(Job.id==id).first()
        company = session.query(Company).join(Job, Company.id == Job.company_id).filter(Job.id==id).first()

        if job:
            clear()
            subheading("Job details")
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
            print("Please select a valid job ID or press enter to go to the main menu")
            id = input()
    
def apply(job, company):
    choice = handle_yes_no("Would you like to apply for this job?")
    if choice:
        applications = session.query(Application).filter(Application.candidate_id==logged_user.id).all()
        if len(applications) < 3:
            application = session.query(Application).filter(and_(Application.job_id==job.id, Application.candidate_id==logged_user.id)).first()
            if application:
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
            print("You've applied for the maximum number of jobs (3). Here are your existing applications:")
            show_applications()
    
    else:
        clear()
        filter_jobs()


def lookup(id,filter_options):
    for option in filter_options:
        if option[0]==id:
            choice = option[1]
            return choice
    return None

def get_category_jobs(category):
    i=1
    for option in category:
        print(f"{option[0]}. {option[1]}")
        i=i+1
    print(f"Please select an option:")
    choice = input().lower()
    if choice.isdigit():
        option_id = int(choice)
        option_name = next((name for id, name in category if id == option_id), None)
        if option_name and category == departments:
            jobs = session.query(Job).filter(func.lower(Job.department) == option_name.lower()).all()
        elif option_name and category == sizes:
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(func.lower(Company.size) == option_name.lower()).all()
        elif option_name and category == industries:
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(func.lower(Company.industry) == option_name.lower()).all()
        else:
            print("Invalid department ID.")
            filter_jobs()
    else:
        if category == departments:
            jobs = session.query(Job).filter(func.lower(Job.department) == choice).all()
        elif category == sizes:
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(func.lower(Company.size) == choice).all()
        else:
            jobs = session.query(Job).join(Company, Job.company_id == Company.id).filter(func.lower(Company.industry) == choice).all()
        if not jobs:
            print("There are no jobs that meet your current criteria")
            filter_jobs()
    show_filtered_jobs(jobs)


def filter_jobs():
    subheading("Filter jobs by:")
    print("""
            1. Industry
            2. Company size
            3. Department
            4. Salary
            Please select an option or 'menu' for main menu""")

    loop = True

    while loop:
        choice = input()

        if choice.lower() == "industry" or choice == "1":
            subheading("Industries")
            get_category_jobs(industries)
            break

        elif choice.lower() == "company size" or choice.lower() == "company" or choice.lower() == "size" or choice == "2":
            subheading("Company Sizes")
            get_category_jobs(sizes)
            break
        
        elif choice.lower() == "department" or choice == "3":
            subheading("Departments")
            get_category_jobs(departments)
            break

        elif choice.lower() == "salary" or choice == "4":
            print("Please enter a minimum salary:")
            min_sal = input()
            jobs = session.query(Job).filter(Job.salary>=min_sal).all()
            show_filtered_jobs(jobs)
            break

        elif choice.lower() == "menu":
            clear()
            break

        else:
            print("Invalid input. Please select again:")



def show_filtered_jobs(jobs):
    clear()
    if len(jobs)>0:
        heading(f"Filtered jobs")
        for job in jobs:
            print(job)
        print("Select an id to show the jobs details, or press enter to go back to the filter menu:")
        choice = input()
        if choice.isdigit():
            job_id = int(choice)
            show_job_details(job_id)
        else:
            filter_jobs()
            
    else:
        print(f"There are no jobs currently available that meet your conditions.")
        filter_jobs()


def view_all_jobs():
    jobs = session.query(Job).all()
    heading("Open jobs")
    print(f"There are {len(jobs)} jobs currently available.")
    x=1
    loop=True
    while loop:
        for job in jobs:
            if job.id>=x and job.id<=x+9:
                print(job)
        if x+9<len(jobs):
            choice = handle_yes_no("View more jobs?")
            if choice:
                x = x+10
            else:
                loop=False
        else:
            print("That's all of the open roles currently available.")
            loop=False


    print("\nWhat would you like to do next?")

    while True:
        print("View a job - please enter the ID of the job you'd like to view")
        print("Filter jobs - select 'filter'")
        print("Menu - back to the main menu")
        choice = input()
        clear() 

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
    clear()
    app_to_delete = session.query(Application).filter(Application.id==id and Application.candidate_id == logged_user.id).first()
    if app_to_delete:
        session.delete(app_to_delete)
        session.commit()
        print(f"Application ID{id} successfully deleted")
    else:
        print(f"You don't appear to have any applications with ID{id}. Here are your current applications:")
        show_applications()


def show_applications():
    loop = True
    while loop:
        applications = session.query(Application).filter(Application.candidate_id==logged_user.id).all()
        if len(applications)>0:
            heading("Current applications")
            for application in applications:
                company = session.query(Company).filter(Company.id == application.job.company_id).first()
                print(f"{application} | {company}")
            choice = handle_yes_no("\nWould you like to withdraw any applications?")
            if choice:
                print(Fore.RED+"Please enter the ID to withdraw:"+Style.RESET_ALL)
                id = input()
                withdraw(id)
            else:
                clear()
                break
        else:
            subheading("Current applications")
            print("You have not applied to any jobs yet\n")
            choice = handle_yes_no("Would you like to view open jobs?")
            clear()
            if choice:
                view_all_jobs()
            break


def update_details():
    user_to_update = session.query(Candidate).filter(Candidate.id==logged_user.id).first()
    choice = handle_yes_no("Update name?")
    if choice: 
        print("Enter updated name:")
        name=input()
        user_to_update.full_name = name
        logged_user.full_name = name
        session.commit()
    choice = handle_yes_no("Update email?")
    if choice:
        print("Enter updated email:")
        email=input()
        valid_email = check_email(email)
        user_to_update.email = valid_email
        logged_user.email = valid_email
        session.commit()
    clear()
    subheading("Your details")
    print(f"{logged_user.full_name} - {logged_user.email}")


def delete_profile():
    global logged_user
    print("Deleting your profile will remove any open applications and log you out")

    choice = handle_yes_no(Fore.RED+"Are you sure you want to delete your profile?"+Style.RESET_ALL)
    if choice:
        user_to_delete = session.query(Candidate).filter(Candidate.id==logged_user.id).first()
        apps_to_delete = session.query(Application).filter(Application.candidate_id==logged_user.id).all()
        session.delete(user_to_delete)
        session.commit()
        for app in apps_to_delete:
            session.delete(app)
            session.commit()
        clear()
        print("Account successfully deleted")
        logged_user = None


def candidate_details():
    subheading("Your details")
    print(f"Name: {logged_user.full_name}\nEmail: {logged_user.email}")
    print("Would you like to 'update' your details or 'delete' your account?")
    loop = True
    while loop:
        choice = input()
        if choice == "update":
            update_details()
            break
        elif choice == "delete":
            delete_profile()
            break
        elif choice == "menu":
            break
        else:
            print("Please enter a valid option. You can select 'update', 'delete' or 'menu':")


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
                    if choice.lower() == "jobs" or choice.lower() == "all" or choice == "1":
                        clear()
                        view_all_jobs()
                        break
                    elif choice.lower() == "filter" or choice == "2":
                        clear()
                        filter_jobs()
                        break
                    elif choice.lower() == "applications" or choice == "3":
                        clear()
                        show_applications()
                        break
                    elif choice.lower() == "account" or choice.lower() == "update" or choice.lower() == "delete" or choice == "4":
                        clear()
                        candidate_details()
                        break
                    elif choice.lower() == "logout" or choice.lower() == "quit" or choice.lower() == "exit" or choice == "5":
                        clear()
                        subheading("Logging out...")
                        loop = False
                        break
                    else:
                        print("Invalid input. Please select again:")
                        choice = input()
    print("Thanks for using the Job Board CLI App!")


if __name__ == "__main__":
    start()