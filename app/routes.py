from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager, db
from app.models import User



@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get data from the form and create a new user
        username = request.form['username']
        password = request.form['password']
        
        # Example: hash the password (use a secure method in production)
        hashed_password = hash_password(password)

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implement login logic
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    # Implement profile logic
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
