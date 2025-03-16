from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Material, ProductionType, Quote, CurrencyRate
from app.forms import QuoteForm
from app.utils.pricing import CostCalculator
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    quotes = Quote.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', quotes=quotes)

@main_bp.route('/new_quote', methods=['GET', 'POST'])
@login_required
def new_quote():
    form = QuoteForm()
    form.material_id.choices = [(m.id, m.name) for m in Material.query.all()]
    form.production_type_id.choices = [(p.id, p.name) for p in ProductionType.query.all()]
    
    if form.validate_on_submit():
        # Salva il file
        file = form.design_file.data
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Calcolo costi
        calculator = CostCalculator(
            form.material_id.data,
            form.production_type_id.data,
            form.quantity.data
        )
        
        try:
            calculator.calculate_nesting(file_path)
            results = calculator.compute_costs(form.currency.data)
            
            # Salva quotazione
            quote = Quote(
                user_id=current_user.id,
                material_id=form.material_id.data,
                production_type_id=form.production_type_id.data,
                quantity=form.quantity.data,
                unit_cost=results['unit_cost'],
                total_cost=results['total_cost'],
                currency=form.currency.data,
                expiration_date=datetime(datetime.now().year, 12, 31)
            )
            
            db.session.add(quote)
            db.session.commit()
            
            return redirect(url_for('main.quote_details', quote_id=quote.id))
            
        except Exception as e:
            flash(f'Errore nel calcolo: {str(e)}')
    
    return render_template('new_quote.html', form=form)