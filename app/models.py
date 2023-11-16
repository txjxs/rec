from flask_login import UserMixin
from app import login_manager, db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Add any other user fields as needed

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
