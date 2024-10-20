import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
