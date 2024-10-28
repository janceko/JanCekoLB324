import os
import sys

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///tasks.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import create_app