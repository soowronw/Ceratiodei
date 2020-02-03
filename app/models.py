from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Captured_data(db.Model):
    __tablename__ = 'captured_data'
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(200))
    ip = db.Column(db.String(16))
    ua = db.Column(db.String(120))
    referrer = db.Column(db.String(200))
    created = db.Column(db.DateTime(), default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    role = db.Column(db.Boolean())


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Links(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer(), primary_key=True)
    route = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(250), nullable=False)
    role = db.Column(db.Boolean(), default=False)