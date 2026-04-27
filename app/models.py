from sqlalchemy import Column, Integer, String
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    movie = Column(String)
    city = Column(String)