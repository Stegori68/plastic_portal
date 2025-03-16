import smtplib
from email.mime.text import MIMEText
from celery import Celery
from app import create_app

app = create_app()
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_email_async(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = to
    
    with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.send_message(msg)

def send_password_reset_email(email, token):
    subject = "Reset Password"
    reset_url = f"https://yourdomain.com/reset_password/{token}"
    body = f"Usa questo link per resettare la password: {reset_url}"
    send_email_async.delay(email, subject, body)