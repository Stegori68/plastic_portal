from flask import Flask, render_template, redirect, url_for, flash, request
from plastic_portal import app, db
from plastic_portal.forms import LoginForm, QuoteForm, RegistrationForm, MaterialForm, ProductionForm, UserForm
from plastic_portal.models import User, Material, Production, Quote
from flask_login import login_user, logout_user, current_user, login_required
from datetime import date
from . import app

@app.route('/')
def index():
    return render_template('index.html')
    # return "Allora funziona!"

@app.route('/login', methods=['GET, POST'])
def login():
    # ... (Logica per la gestione del login) ...
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    # ... (Logica per la gestione del logout) ...
    return redirect(url_for('index'))

@app.route('/quote', methods=['GET, POST'])
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

# ... (Altre rotte per la gestione di utenti, materiali, lavorazioni, ecc.) ...