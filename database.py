import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI', 'sqlite:///my-flask-app-database.db')

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
