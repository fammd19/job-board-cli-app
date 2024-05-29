from lib.env import session, fake
from lib.models import Application, Candidate, Company, Job
from random import choice, randrange, randint



departments = ["Finance","Human Resources","Marketing","Operations","Sales","Technology"]
industries = ["Agriculture","Construction","Education","Financial Services","Food & Beverage","Healthcare","Hopitality","Insurance","Legal Services","Manufactuting","Media & Entertainment","Professional Services","Real Estate","Retail","Recruitment","Technology"]
titles = ["Associate","Executive","Director","Head Of","Junior","Manager","Senior Manager"]
sizes = ["1-10","11-50","51-100","101-200","200-500","500+"]


def create_companies():
    companies = [Company (
            name = fake.company(),
            industry = choice(industries),
            size = choice(sizes)
        ) for i in range (15)]

    session.add_all(companies)
    session.commit()

    return companies


def create_jobs():

    jobs = [ Job (
            title = choice(titles),
            salary = randrange(0,200000,1000),
            department = choice(departments),
            date_posted = fake.date(),
            city = fake.city(),
            company_id = randint(1,15)
        ) for i in range (30)]

    session.add_all(jobs)
    session.commit()

    return jobs


def delete_records():
    session.query(Application).delete()
    session.query(Candidate).delete()
    session.query(Company).delete()
    session.query(Job).delete()

    session.commit()

    