# Job Board CLI App
Thanks for taking a look at my repo. This app is a submission for my phase 3 project with Academy XI.

## Introduction
The Job Board CLI App is a python app designed to mimic a simplified job site, where a user, acting as a candidate, can create an account, browse, and apply for jobs. This is something I hope to expand upon to build out a fully fledged job site. 

## Installation
1. Clone the repo to your local machine
2. Run the following commands:
    - `pipenv install & pipenv shell`
    - `alembic upgrade head`\
    This will create the models and seed the jobs and companies tables in the database
3. To start the app, from the root directory run:
    `python lib/run.py`
