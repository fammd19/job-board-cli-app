from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Job (Base):
    __tablename__ = "jobs"

    id = Column (Integer(), primary_key=True)
    title = Column (String(), nullable=False)
    salary = Column (Integer())
    department = Column (String(), nullable=False)
    date_posted = Column (String(), nullable=False)
    city = Column (String(), nullable=False)

    #one-to-many link for company to jobs
    company_id = Column(Integer(), ForeignKey("companies.id"))

    #many-to-many link for jobs to candidates through applications
    applications = relationship("Application", back_populates="job")
    candidates = association_proxy("applications", "candidate", creator = lambda c: Application(candidate=c))

    def __repr__(self):
        return f"{self.id}: {self.title}, {self.city}"
    

class Candidate (Base):
    __tablename__ = "candidates"
    id = Column (Integer(), primary_key=True)
    full_name = Column (String(), nullable=False)
    email = Column (String(), nullable=False)

    #many-to-many link for candidates to jobs through applications
    applications = relationship("Application", back_populates="candidate")
    jobs = association_proxy("applications", "job", creator = lambda j: Application(job=j))

    def __repr__(self):
        return f"{self.id}: {self.first_name} {self.family_name}, {self.profession}"

class Company (Base):
    __tablename__ = "companies"

    id = Column (Integer(), primary_key=True)
    name = Column (String(), nullable=False)
    industry = Column (String(), nullable=False)
    size = Column (String())

    #one-to-many link for company to jobs
    jobs = relationship("Job", backref=backref("company"))

    def __repr__(self):
        return f"{self.id}: {self.name}, {self.industry}"

class Application (Base):
    __tablename__ = "applications"

    id = Column (Integer(), primary_key=True)

    job_id = Column (Integer(), ForeignKey("jobs.id"))
    candidate_id = Column (Integer(), ForeignKey("candidates.id"))

    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")

    def __repr__(self):
        return f"ID: {self.id} | Job ID: {self.job_id} | Candidate ID: {self.candidate_id}"
