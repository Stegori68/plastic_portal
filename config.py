import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ooysdvf9879ffkkfifihif1441'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://admin:%Onafets01!@plastic-portal-db.czw0aqcke793.eu-north-1.rds.amazonaws.com:3306/plastic_portal_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'