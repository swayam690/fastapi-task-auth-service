from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key = True, index = True)
    username = Column(String , unique = True, index = True)
    password = Column(String)
    