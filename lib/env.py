from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import os

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
