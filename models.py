from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from database import engine

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    roll_number = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
