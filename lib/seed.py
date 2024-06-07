from lib.env import session, fake, departments, industries, titles, sizes
from lib.models import Application, Candidate, Company, Job
from random import choice, randrange, randint


def create_companies():
    companies = [Company (
            name = fake.company(),
            industry = choice(industries),
            size = choice(sizes)
        ) for i in range (10)]

    session.add_all(companies)
    session.commit()

    return companies


def create_jobs():

    jobs = [ Job (
            title = choice(titles),
            salary = randrange(0,200000,1000),
            department = choice(departments),
            date_posted = fake.date_this_year(),
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

    