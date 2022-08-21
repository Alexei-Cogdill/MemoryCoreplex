import os
from flask import Flask
from flask_jsglue import JSGlue
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Resource, Api

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
jsglue = JSGlue(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'
