from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from main_config import Config


app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
login_manager: LoginManager = LoginManager(app)
db = SQLAlchemy(app)


from app import routes
