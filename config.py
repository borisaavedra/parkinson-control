import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_CYAN_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False