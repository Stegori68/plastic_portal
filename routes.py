from flask import Flask, render_template, redirect, url_for, flash, request
from plastic_portal import app, db
from plastic_portal.forms import LoginForm, QuoteForm, RegistrationForm, MaterialForm, ProductionForm, UserForm
from plastic_portal.models import User, Material, Production, Quote
from flask_login import login_user, logout_user, current_user, login_required
from datetime import date
from . import app
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('index.html')
    # return "Allora funziona!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione avvenuta con successo! Puoi effettuare il login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrazione', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Create an instance of LoginForm
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login fallito. Controlla email e password.', 'danger')
            return render_template('login.html', title='Login', form=form) # Pass the form to the template
    return render_template('login.html', title='Login', form=form) # Pass the form to the template

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    form = QuoteForm()
    if form.validate_on_submit():
        # ... (Logica per il calcolo del preventivo, nesting, ecc.) ...
        return redirect(url_for('quote_result', quote_id=new_quote.id))
    return render_template('quote_form.html', title='Preventivo', form=form)

@app.route('/quote/<int:quote_id>')
@login_required
def quote_result(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return render_template('quote_result.html', title='Risultato Preventivo', quote=quote)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

@app.route('/admin/users')
@login_required
def user_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    users = User.query.all()
    return render_template('admin/user_management.html', users=users)

@app.route('/admin/materials')
@login_required
def material_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    materials = Material.query.all()
    return render_template('admin/material_management.html', materials=materials)

@app.route('/admin/productions')
@login_required
def production_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    materials = Material.query.all()
    return render_template('admin/production_management.html', productions=productions)


# ... (Altre rotte per la gestione di utenti, materiali, lavorazioni, ecc.) ...