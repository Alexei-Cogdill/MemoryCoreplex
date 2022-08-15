from init import db, login_manager, api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_restful import Resource, Api


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True)
    display_name = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_Admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', backref='post')
    scores = db.relationship('Score', backref='postt')

    def __init__(self, name, display_name, email, password, is_Admin):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_Admin = is_Admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'name':self.name, 'display_name':self.display_name, 'email':self.email, 'password_hash':self.password_hash, 'is_Admin':self.is_Admin}

class Review(db.Model):

    __tablename__ = "reviews"


    review_id = db.Column(db.Integer, primary_key=True)
    reviewTitle = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    def __init__(self, reviewTitle, summary, is_approved, user_id):
        self.reviewTitle = reviewTitle
        self.summary = summary
        self.is_approved = is_approved
        self.user_id = user_id

    def json(self):
        return {'reviewTitle':self.reviewTitle, 'summary':self.summary, 'is_approved':self.is_approved}

class Score(db.Model):

    __tablename__ = "scores"

    score_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    def __init__(self, score, time, user_id):
        self.score = score
        self.time = time
        self.user_id = user_id

    def json(self):
        return {'score':self.score, 'time':self.time, 'display_name':post.display_name}
