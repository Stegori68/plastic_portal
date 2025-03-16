from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    quotes = db.relationship('Quote', backref='author', lazy=True)
    last_password_reset = db.Column(db.DateTime)
    # Altri campi...

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    thickness = db.Column(db.Float)
    cost = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    # Altri campi...

class ProductionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(20))  # 'plotter' o 'fustella'
    setup_cost = db.Column(db.Float)
    cutting_cost = db.Column(db.Float)
    tooling_cost = db.Column(db.Float)  # Solo per fustella

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(100), unique=True)
    expires = db.Column(db.DateTime)