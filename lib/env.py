from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import os

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

departments = ["Finance","Human Resources","Marketing","Operations","Sales","Technology"]
industries = ["Agriculture","Construction","Health & Education","Financial Services","Hospitality","Legal","Manufactuting","Retail","Technology"]
titles = ["Associate","Executive","Director","Head Of","Junior","Manager","Senior Manager"]
sizes = ["1-10","11-50","51-100","101-200","200-500","500+"]

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def wait():
    os.wait()
