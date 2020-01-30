from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


appFlask = Flask(__name__)
appFlask.config.from_object('config')
db = SQLAlchemy(appFlask)
login_manager = LoginManager(appFlask)


from app import views, models
