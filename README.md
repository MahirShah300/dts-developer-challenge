# dts-developer-challenge
dts developer challenge to make a system for workers to track and manage their tasks.

## Overview
This application is written in python using FastAPI for the backend, SQLite and SQLalchemy for the database, 
and Jinja templates with HTML for the frontend.

## Installation
First clone the repository with the git command `git clone git@github.com:MahirShah300/dts-developer-challenge.git`
To install all the dependencies, first use the command `pip install pipenv` if it is not already installed.
Then run the command `pipenv install` to install the dependencies. Then run `pipenv shell` to initalise the virtual environment
To then run the application, use the command `fastapi dev main.py` then follow the link shown in the terminal.

## Instructions
Users can use the buttons on the pages to enter tasks into the database, search for tasks by id,
search for tasks by title or partial title, show tasks by status, and search by title and status.
They will also be able to edit and delete tasks. 

## Further Development
Create a more fluid and appealing front end using more powerful technologies such as flask or react.
With these as a front end, can then start taking more advantage of APIs, and use JSON endpoints to take advantage of pydantic to validate and represent task objects, and for the auto generated documentaions.
