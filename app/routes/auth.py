from flask import Blueprint, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models import User, PasswordResetToken
from app.forms import LoginForm, RegistrationForm, ResetPasswordForm
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        flash('Login non valido')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = secrets.token_urlsafe()
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=token,
                expires=datetime.utcnow() + timedelta(hours=1)
            )
            db.session.add(reset_token)
            db.session.commit()
            send_password_reset_email(user.email, token)
        flash('Se l\'email esiste, ti invieremo le istruzioni')
    return render_template('auth/reset_request.html', form=form)