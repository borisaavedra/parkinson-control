import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_CYAN_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FEELINGS = [
        "Ansiedad",             # 0
        "Rigidez",              # 1
        "Temblor",              # 2
        "Lentitud",             # 3
        "Depresión",            # 4
        "Palpitaciones",        # 5
        "Salivación",           # 6
        "Más ganas de orinar",  # 7
        "Sudoración"            # 8
    ]