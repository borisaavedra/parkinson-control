from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from flask_login import UserMixin
from datetime import datetime
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "user_parkinson"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    email = db.Column(db.String(200), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    statuses = db.relationship("ParkinsonControl", backref="patient", lazy="dynamic")
    feelings = db.relationship("Feeling", backref="patient", lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.name)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))



class ParkinsonControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    starttime = db.Column(db.DateTime(timezone=True), index=True, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user_parkinson.id"))

    def __repr__(self):
        return '<Control {} {}>'.format(self.status, self.starttime)


class Feeling(db.Model):
    __tablename__ = "feeling"
    id = db.Column(db.Integer, primary_key=True)
    feeling = db.Column(db.String(200), unique=True, nullable=False)
    strattime = db.Column(db.DateTime(timezone=True), index=True, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user_parkinson.id"))

    def __repr__(self):
        return '<Feeling {}>'.format(self.feeling)