from plastic_portal import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    quotes = db.relationship('Quote', backref='author', lazy=True)
    logs = db.relationship('Log', backref='created_logs', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.role}')"

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    dimensions = db.Column(db.String(255))
    thickness = db.Column(db.Numeric(5, 2))
    quotes = db.relationship('Quote', backref='related_quotes', lazy=True)

    def __repr__(self):
        return f"Material('{self.name}')"

class Production(db.Model):
    __tablename__ = 'productions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    setup_cost = db.Column(db.Numeric(10, 2), nullable=False)
    cutting_cost_per_sheet = db.Column(db.Numeric(10, 2), nullable=False)
    quotes = db.relationship('Quote', backref='production_quotes', lazy=True)

    def __repr__(self):
        return f"Production('{self.name}')"

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False)
    quantity_requested = db.Column(db.Integer, nullable=False)
    element_dimensions = db.Column(db.String(255))
    drawing_path = db.Column(db.String(255))
    order_multiple = db.Column(db.Integer)
    cost_per_element = db.Column(db.Numeric(10, 4))
    selling_price = db.Column(db.Numeric(10, 4))
    quote_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.Date)
    currency = db.Column(db.String(10), default='EUR')
    exchange_rate = db.Column(db.Numeric(10, 4))
    material = db.relationship('Material', backref='quotes', lazy=True)
    production_type = db.relationship('Production', backref='quotes', lazy=True)

    def __repr__(self):
        return f"Quote('{self.id}', '{self.quantity_requested}')"

class ExchangeRate(db.Model):
    __tablename__ = 'exchange_rates'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), unique=True, nullable=False)
    rate = db.Column(db.Numeric(10, 4), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ExchangeRate('{self.currency}', '{self.rate}')"

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Text)

    def __repr__(self):
        return f"Setting('{self.name}', '{self.value}')"

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"Log('{self.timestamp}', '{self.activity}')"