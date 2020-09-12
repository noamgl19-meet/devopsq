from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.types import BINARY


Base = declarative_base()

#requests
class Reqs(Base):
    __tablename__ = "reqs"
    id = Column(Integer, primary_key = True)
    student = Column(String)
    question = Column(String)
    answered = Column(Boolean)
    place = Column(Integer)
    date = Column(String)

    def __repr__(self):
    	message = "\nid: " +str(self.id)+ "\nusername: " + self.student + "\nquestion: " + self.question + "\nanswered: " + str(self.answered)
    	return message

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)
    role = Column(String)
    counter = Column(Integer)
    requests = Column(Integer)