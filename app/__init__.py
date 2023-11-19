from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main_config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main_config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
login_manager: LoginManager = LoginManager(app)


from app import routes


from app import routes
