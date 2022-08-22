from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from models import User, Review, Score

class ScoreForm(FlaskForm): #Form used in html page to submit score data to db
    score = StringField('Score', validators=[DataRequired()])
    submit = SubmitField("Submit Score")

class LoginForm(FlaskForm):#Form used in html page to submit login data to db
    email = StringField('Email', validators=[DataRequired("Please enter a valid email")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a valid password")])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm): #Form used in html page to submit registration data to db
    name = StringField('Name', validators=[DataRequired("Please enter your full name")])
    display_name = StringField('Display Name', validators=[DataRequired("Please enter a display name")])
    email = StringField('Email', validators=[DataRequired("Please enter your email"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password"), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired("Please re-enter your password")])
    submit = SubmitField('Register!')

    def validate_email(self, email): #validates if email has already been registered
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been already registered!')

    def validate_displayName(self, display_name): #validates if display name has already been used
        if User.query.filter_by(display_name=display_name.data).first():
            raise ValidationError('This display name is already taken!')

class ReviewForm(FlaskForm): #Form used in html page to submit review data to db
    reviewTitle = StringField('Review Title', validators=[DataRequired("Please enter a review title")])
    summary = StringField('Review Summary', validators=[DataRequired("Please enter a summary for your review")])
    submit = SubmitField('Submit Review')
