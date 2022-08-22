from init import app, db, api
from flask import render_template, redirect, request, url_for, flash, abort, jsonify, make_response
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Review, Score
from forms import LoginForm, RegistrationForm, ReviewForm, ScoreForm
from nltk import flatten
#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_restful import Resource, Api
from flask_jsglue import JSGlue
import requests
import json
import random

#admin = Admin(app)
#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Review, db.session))
#admin.add_view(ModelView(Score, db.session))

@app.route('/games') #Routes to the games page
@login_required
def games():
    return render_template('games.html')

@app.route('/games/numbergame', methods=['GET', 'POST']) #Routes to the actual game page
@login_required
def numbergame(): #Function that submits user score data to database

    form = ScoreForm()
    if form.validate_on_submit():
        if int(form.score.data) > 0:
            score = Score(score=form.score.data,
                user_id=current_user.id
                )
            db.session.add(score)
            db.session.commit()
            flash("Score Submitted", "primary")
            return redirect(url_for('games'))
        elif int(form.score.data) == 0: #Checks score data if it is 0 - doesn't commit to db
            flash("Did not score", "primary")
            return redirect(url_for('games'))
    elif len(form.errors.items()) > 0: #Returns any errors that are present
        randomValue = flatten(list(form.errors.values()))
        for i in randomValue:
            flash(i, "danger")
        return redirect(url_for('games'))
    return render_template('numbergame.html', form=form)

@app.route('/about') #Routes to about page
def about():
    return render_template('about.html')

@app.route('/profile/<string:display_name>', methods=['GET', 'POST']) #Routes to user profile's page
@login_required
def profile(display_name): #Gets json data from API Resource and uses it to render data in html file
    us = GetProfile()
    user = us.get(display_name)
    return render_template('profile.html', user=user)

@app.route('/leaderboard') #Routes to leaderboard page
@login_required
def leaderboard(): #Grabs all user scores in a descending order and stores in table to pass to html page
    scores = Score.query.order_by(Score.score.desc()).all()
    ddl = []
    for score in scores:
        ddl.append(score)
    return render_template('leaderboard.html', ddl=ddl)

@app.route('/profile/userScore', methods=['GET', 'POST']) #Routes to users profile scores
@login_required
def userScore(): #Queries database by score for the user scores and stores in table to pass to html page
    scores = Score.query.filter(Score.score).order_by(Score.score.desc())
    ddl = []
    for score in scores:
        ddl.append(score)
    return render_template('userScores.html',ddl=ddl)

@app.route('/approveReview', methods=['GET', 'POST']) #Routes to the admin page for approving reviews submitted by users
@login_required
def approveReview(): #Queries all reviews to render in html page
    users = Review.query.all()
    return render_template('approveReview.html', users=users)

@app.route('/flip', methods=['POST']) #Routes to page that accepts the review
@login_required
def flip(): #Updates review and posts review if accepted
    review = Review.query.filter_by(review_id=request.form["flip"]).first()
    review.is_approved = True
    db.session.commit()
    return redirect(url_for('approveReview'))

@app.route('/flip2', methods=['POST']) #Routes to page that denies the review
@login_required
def flip2(): #Updates review and deletes review if denied
    review2 = Review.query.filter_by(review_id=request.form["flip2"]).first()
    review2.is_approved = False
    db.session.delete(review2)
    db.session.commit()
    return redirect(url_for('approveReview'))

@app.route('/userHome', methods=['GET']) #Routes to the user's welcome page when logging in
@login_required
def welcome_user():
    return render_template('home.html')

@app.route('/adminHome', methods=['GET', 'POST'])#Routes to the admin's welcome page when logging in
@login_required
def welcome_admin():
    return render_template('home.html')

@app.route('/reviews', methods=['GET', 'POST']) #Routes to the reviews page
def reviews(): #Queries all reviews to render in html page
    users = Review.query.all()
    return render_template('reviews.html', users=users)

@app.route('/createReview', methods=['GET', 'POST']) #Routes to creat a review page
@login_required
def createReview(): #Review form that is used to post user inputted data to database

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(reviewTitle=form.reviewTitle.data,
                    summary=form.summary.data,
                    user_id=current_user.id,
                    is_approved=False)
        db.session.add(review)
        db.session.commit()
        flash("Review Submitted", "primary")
        return redirect(url_for('reviews'))
    elif len(form.errors.items()) > 0:
        randomValue = flatten(list(form.errors.values()))
        for i in randomValue:
            flash(i, "danger")
        return redirect(url_for('createReview'))
    return render_template('createReview.html', form=form)

@app.route('/logout') #Routes to the logout page and logs user out
@login_required
def logout():
    logout_user()
    flash("You logged out!", "primary")
    return redirect(url_for('homecontroller'))

@app.route('/login', methods=['GET', 'POST']) #Routes to the login page
def login(): #Login form that is used to post user inputted data to database

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            if user.is_Admin:
                login_user(user)
                flash('Welcome Admin!', 'primary')

                return redirect(url_for('welcome_admin'))
            else:
                login_user(user)
                flash('Welcome User!', 'primary')

                next = request.args.get('next')

                if next == None or not next[0]=='/':
                    next = url_for('welcome_user')

                    return redirect(next)
        else:
            flash('Invalid username or password', 'danger')
    elif len(form.errors.items()) > 0:
        randomValue = flatten(list(form.errors.values()))
        for i in randomValue:
            flash(i, "danger")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST']) #Routes to the register page
def register(): #Login form that is used to post user inputted data to database
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(name=form.name.data,
                    display_name=form.display_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    is_Admin=False)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!", "primary")
        return redirect(url_for('login'))
    elif len(form.errors.items()) > 0:
        randomValue = flatten(list(form.errors.values()))
        for i in randomValue:
            flash(i, "danger")
        return redirect(url_for('register'))

    return render_template('register.html', form=form)


class GetUser(Resource): #Restful Flask API for getting user data
    def get(self, display_name):

        user = User.query.filter_by(display_name=display_name).first()

        if user:
            return user.json()
        else:
            return {'Could not get user'}, 404
class GetProfile(Resource): #Restful Flask API for getting profile data by display_name
    def get(self, display_name):

        profile = User.query.filter_by(display_name=display_name).first()
        if profile:
            return profile.json()
        else:
            abort(404, description="Unable to load profile data")


class getReview(Resource): #Restful Flask API for getting review data by id
    def get(self, review_id):

        review = Review.query.filter_by(review_id=review_id).first()

        if review:
            return review.json()
        else:
            return {"No reviews available"}, 404

class homeController(Resource):
    def __init__(self):
        pass
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)

api.add_resource(GetUser,'/users/<string:display_name>')
api.add_resource(GetProfile,'/profile/<string:display_name>')
api.add_resource(getReview,'/reviews/<int:review_id>')
api.add_resource(homeController, '/')
