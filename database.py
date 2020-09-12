from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

def con():
    engine = create_engine('sqlite:///space.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def add_request(con, student, question):
    session = con
    i = session.query(Reqs).filter_by(answered = False).all()
    if len(i) > 0:
        i = i[-1].place + 1
    else:
        i = 0
    req = Reqs(student = student, question = question, answered = False, place = i, date = str(datetime.datetime.now())[0:10])
    session.add(req)
    session.commit()

def add_r(con, student):
    session = con
    get_user(session, student).requests += 1
    session.commit()

def get_student_reqs(con, student):
    session = con
    reqs = session.query(Reqs).filter_by(student = student, answered = False).all()
    return reqs

def get_reqs(con):
    session = con
    return session.query(Reqs).filter_by(answered = False).all()

def get_first_req(con, student):
    session = con
    req = session.query(Reqs).filter_by(student = student).first()
    return req

def update(con, id, username):
    session = con
    student = session.query(Reqs).filter_by(id = id).first().student
    student = get_first_req(con, student)
    student.answered = True
    student.student = "answered"
    session.commit()
    reqs = get_reqs(con)
    for r in reqs:
        r.place -= 1
        session.commit()
    
    get_user(con,username).counter += 1
    session.commit()

def add_user(con, username, password, role):
    session = con
    user = Users(username = username, password = password, role = role, counter = 0, requests = 0)
    session.add(user)
    session.commit()

def get_all_students(con):
    session = con
    return session.query(Users).filter_by(role = "student").all()

def get_student(con, username):
    session = con
    student = session.query(Users).filter_by(username = username).first()
    return student

def get_user(con, username):
    session = con
    user = session.query(Users).filter_by(username = username).first()
    return user

def check_username(con, username):
    session = con
    users = session.query(Users).filter_by(username = username).all()
    if len(users) > 0:
        return True
    else:
        return False

def check_password(username, password):

    if check_username(con(), username):
        if get_student(con(), username).password == password:
            return True

    return False

names = ["comer", "cguy", "cpaz", "cron", "clior", "cnoa"]
for name in names:

    add_user(con(), name, "a123456", "teacher")

add_user(con(), "computer", "a123456", "student")