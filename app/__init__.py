from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somekey@letmelogin@1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['LOGIN_VIEW'] = 'login'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes
