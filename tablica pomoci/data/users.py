from sqlalchemy import Column, Integer, String, DateTime
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    modified_date = Column(DateTime, nullable=True)