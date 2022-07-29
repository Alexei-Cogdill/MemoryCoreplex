from init import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from forms import LoginForm, RegistrationForm
from nltk import flatten
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(User, db.session))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcomeUser.html')

@app.route('/adminHome')
@login_required
def welcome_admin():
    return render_template('admin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!", "primary")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            if user.is_Admin:
                login_user(user)
                flash('Logged in successfully!', 'primary')

                return redirect(url_for('welcome_admin'))
            else:
                login_user(user)
                flash('Logged in successfully!', 'primary')

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


@app.route('/register', methods=['GET', 'POST'])
def register():
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

@app.route('/adminHome', methods=['GET', 'POST'])
@login_required
def adminView():
    if current_user.admin:
        return render_template('admin.html')
    else:
        return render_template('home.html')
