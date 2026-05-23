from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)


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
    res_id = db.Column(db.Integer, db.ForeignKey('resources.res_id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), default="Any", nullable=True)
    type = db.Column(db.String, nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    img = db.Column(db.String, default="Book.jpg", nullable=True)
    status = db.Column(db.String, default="Pending", nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    requestor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class Trades(db.Model):
    __tablename__='trades'

    t_id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, db.ForeignKey('resources.res_id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tokens_exchanged = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

