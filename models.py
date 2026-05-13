from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

class User(db.Model):
    __tablename__='users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, nullable=True)
    branch = db.Column(db.String, nullable=False)
    semester = db.Column(db.String, nullable=False)

class Resource(db.Model):
    __tablename__='resources'

    res_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    token = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String, default="Available")
    img = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Requests(db.Model):
    __tablename__='requests'

    req_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), default="Any", nullable=True)
    type = db.Column(db.String, nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    img = db.Column(db.String, default="Book.jpg", nullable=True)
    status = db.Column(db.String, default="Pending", nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    requestor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)



