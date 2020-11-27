import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nunca-adivinaras-esto"
    SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_CYAN_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False