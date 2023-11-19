from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from flask_login import login_required, current_user, login_user
from app.models import Movie, Rating, User
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/protected')
@login_required
def protected():
    # Your protected route logic here
    return render_template('protected.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/recommendations')
@login_required
def recommendations():
    # Get user's rated movies
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()

    # Create a DataFrame with user ratings
    ratings_data = pd.DataFrame([(rating.user_id, rating.movie_id, rating.rating) for rating in user_ratings],
                                columns=['user_id', 'movie_id', 'rating'])

    # Merge user ratings with movie data
    movie_data = pd.DataFrame([(movie.id, movie.title, movie.genre) for movie in Movie.query.all()],
                              columns=['movie_id', 'title', 'genre'])

    user_movie_ratings = pd.merge(ratings_data, movie_data, on='movie_id')

    # Create a user-movie matrix
    user_movie_matrix = user_movie_ratings.pivot_table(index='user_id', columns='title', values='rating')

    # Fill NaN values with 0
    user_movie_matrix = user_movie_matrix.fillna(0)

    # Calculate cosine similarity between movies
    movie_similarity = cosine_similarity(user_movie_matrix.T)

    # Get the most similar movies
    similar_movies = pd.DataFrame(movie_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

    # Get movies the user hasn't rated
    unrated_movies = user_movie_matrix.columns[user_movie_matrix.loc[current_user.id] == 0]

    # Calculate a weighted average of ratings for unrated movies
    weighted_average = (similar_movies[unrated_movies] * user_movie_matrix.loc[current_user.id]).sum(axis=0) / (
            similar_movies[unrated_movies].sum(axis=0) + 1e-10)

    # Get top recommended movies
    recommended_movies = weighted_average.sort_values(ascending=False).head(5)

    return render_template('recommendations.html', movies=recommended_movies)
if __name__ == '__main__':
    app.run()
