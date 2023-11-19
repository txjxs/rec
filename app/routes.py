from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import RegistrationForm
from flask_login import login_required

from app import app

@app.route('/')
def index():
    return 'Hello, World!'




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add user registration logic here
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login')
def login():
    # Add login logic here
    return render_template('login.html')

@app.route('/protected')
@login_required
def protected():
    # Your protected route logic here
    return render_template('protected.html')

if __name__ == '__main__':
    app.run()
