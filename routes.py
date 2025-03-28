from flask import Flask, render_template, redirect, url_for, flash, request, current_app, send_file
from plastic_portal import app, db
from plastic_portal.forms import LoginForm, QuoteForm, RegistrationForm, MaterialForm, ProductionForm
from plastic_portal.forms import UserForm, ProductCategoryForm, ProductBrandForm, SettingForm, ExchangeRateForm
from plastic_portal.models import User, Material, Production, Quote, ProductCategory, ProductBrand, Setting, ExchangeRate
from flask_login import login_user, logout_user, current_user, login_required
from datetime import date
from . import app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
import csv
import io
import decimal
from flask_mail import Message
from plastic_portal import mail
from decimal import Decimal

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

# @app.route('/quote', methods=['GET', 'POST'])
# @login_required
# def quote():
#     form = QuoteForm()
#     materials = Material.query.join(ProductBrand).join(ProductCategory).order_by(ProductBrand.name, ProductCategory.name, Material.name).all()
#     form.material_type.choices = [(material.id, f"{material.brand.name} - {material.category.name} - {material.name} (sp. {material.thickness} mm)") for material in materials]
#     form.production_type.choices = [(production.id, production.name) for production in Production.query.all()]
#     if form.validate_on_submit():
#         # ... (Logica per il calcolo del preventivo, nesting, ecc.) ...
#         return redirect(url_for('quote_result', quote_id=new_quote.id))
#     return render_template('quote_form.html', title='Preventivo', form=form)

@app.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    form = QuoteForm()
    form.material_type.choices = [(material.id, f"{material.brand.name} - {material.category.name} - {material.name} - (sp. {material.thickness} mm)") for material in Material.query.join(ProductBrand).join(ProductCategory).order_by(ProductBrand.name, ProductCategory.name, Material.name).all()]
    form.production_type.choices = [
        ('best', 'Valuta la soluzione più conveniente'),
        ('compare', 'Confronta più soluzioni'),
        ('Taglio passante a plotter', 'Taglio passante a plotter'),
        ('Taglio passante a fustella testa piana', 'Taglio passante a fustella testa piana'),
        ('Mezzo taglio a rotativa', 'Mezzo taglio a rotativa')
    ]
    form.currency_type.choices = [
        ('EUR', 'Euro'),
        ('USD', 'Dollaro USA')
    ]

    if form.validate_on_submit():
        material_id = form.material_type.data
        currency = form.currency_type.data
        element_dimension_x = form.element_dimension_x.data
        element_dimension_y = form.element_dimension_y.data
        quantity_requested = form.quantity.data
        drawing_file = form.drawing.data
        production_type_choice = form.production_type.data
        fustella_productions = form.fustella_productions.data
        fustella_productions = decimal.Decimal(fustella_productions)

        material = Material.query.get_or_404(material_id)
        profit_margin_setting = Setting.query.filter_by(name='profit_margin').first()
        profit_margin = decimal.Decimal(profit_margin_setting.value) if profit_margin_setting else decimal.Decimal('0.20')

        results = []

        production_methods = []
        if production_type_choice == 'best' or production_type_choice == 'compare':
            production_methods = [
                'Taglio passante a plotter',
                'Taglio passante a fustella testa piana',
                'Mezzo taglio a rotativa'
            ]
        else:
            production_methods = [production_type_choice]

        for method_name in production_methods:
            production = Production.query.filter_by(name=method_name).first()
            if production:
                setup_cost = decimal.Decimal(str(production.setup_cost))
                cutting_cost_per_sheet = decimal.Decimal(str(production.cutting_cost_per_sheet))

                # --- Placeholder for reading drawing and getting shape ---
                element_width = element_dimension_x
                element_length = element_dimension_y
                if drawing_file:
                    filename = secure_filename(drawing_file.filename)
                    # Save the file temporarily (you might want to process it without saving)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    drawing_file.save(file_path)
                    # --- Implement logic in utils/pdf_dxf_parser.py to extract dimensions ---
                    # extracted_dimensions = extract_dimensions(file_path)
                    # if extracted_dimensions:
                    #     element_width = extracted_dimensions['width']
                    #     element_height = extracted_dimensions['height']
                    # os.remove(file_path) # Clean up the temporary file
                    pass # Replace with actual drawing processing

                # --- Placeholder for nesting logic in utils/nesting_utils.py ---
                sheet_width = material.width
                sheet_length = material.length
                useful_width = sheet_width - (Decimal(Setting.query.filter_by(name='useless_margin').first().value))*2
                useful_length = sheet_length - (Decimal(Setting.query.filter_by(name='useless_margin').first().value))*2
                parts_bylenght_1 = useful_length // element_length
                parts_bywidth_1 = useful_width // element_width
                parts_bylenght_2 = useful_length // element_width
                parts_bywidth_2 = useful_width // element_length
                if parts_bylenght_1 * parts_bywidth_1 > parts_bylenght_2 * parts_bywidth_2:
                    elements_per_sheet = parts_bylenght_1 * parts_bywidth_1
                else:
                    elements_per_sheet = parts_bylenght_2 * parts_bywidth_2

                # elements_per_sheet = 1 # Replace with actual nesting calculation
                # elements_per_sheet = perform_nesting(element_width, element_height, sheet_width, sheet_length)

                if elements_per_sheet > 0:
                    num_sheets_needed_exact = quantity_requested / elements_per_sheet
                    num_sheets_needed = int(num_sheets_needed_exact) + (1 if num_sheets_needed_exact > int(num_sheets_needed_exact) else 0)
                    order_multiple = elements_per_sheet
                    total_elements = order_multiple * num_sheets_needed
                    num_sheets_needed_decimal = decimal.Decimal(str(num_sheets_needed))
                    total_elements_decimal = decimal.Decimal(str(total_elements))

                    # --- Calculate Costs ---
                    tooling_cost = 0
                    tooling_cost_per_production = decimal.Decimal(str(tooling_cost_per_production)) if 'tooling_cost_per_production' in locals() and tooling_cost_per_production is not None else decimal.Decimal('0')
                    cutting_cost_times_sheets = cutting_cost_per_sheet * num_sheets_needed_decimal
                    cutting_cost_times_sheets = decimal.Decimal(str(cutting_cost_times_sheets))
                    if method_name.startswith("Taglio passante a fustella") or method_name.startswith("Mezzo taglio a fustella"):
                        fustella_tooling_cost_setting = Setting.query.filter_by(name='fustella_tooling_cost').first()
                        tooling_cost = float(fustella_tooling_cost_setting.value) if fustella_tooling_cost_setting else 400
                        tooling_cost = decimal.Decimal(str(tooling_cost))
                        tooling_cost_expressed = tooling_cost / decimal.Decimal(str(0.8)) # Example calculation
                        tooling_cost_per_production = tooling_cost / total_elements_decimal / fustella_productions if fustella_productions > 0 else tooling_cost
                    setup_cost = decimal.Decimal(str(setup_cost))
                    tooling_cost_per_production = round(decimal.Decimal(str(tooling_cost_per_production)), 3)
                    numerator = setup_cost + cutting_cost_times_sheets + tooling_cost_per_production
                    cost_total_production_with_tooling = numerator / total_elements_decimal if total_elements_decimal > 0 else decimal.Decimal('0')
                    cost_total_production_with_tooling = decimal.Decimal(str(cost_total_production_with_tooling))
                    cost_total_production_no_tooling = (setup_cost + cutting_cost_times_sheets) / total_elements_decimal if total_elements_decimal > 0 else decimal.Decimal('0')
                    cost_total_production_no_tooling = decimal.Decimal(str(cost_total_production_no_tooling))
                    if material.currency != 'EUR':
                        exchange_rate = ExchangeRate.query.filter_by(currency=material.currency).first()
                        material_cost = material.cost_per_unit / exchange_rate.rate
                    cost_material = (material_cost * num_sheets_needed) / total_elements if total_elements > 0 else 0
                    cost_per_element_no_tooling = cost_total_production_no_tooling + cost_material
                    cost_per_element_with_tooling = cost_total_production_with_tooling + cost_material
                    selling_price_no_tooling = cost_per_element_no_tooling / (1 - profit_margin)
                    selling_price_with_tooling = cost_per_element_with_tooling / (1 - profit_margin)
                    if currency != 'EUR':
                        exchange_rate = ExchangeRate.query.filter_by(currency=currency).first()
                        selling_price_no_tooling = selling_price_no_tooling * exchange_rate.rate
                        selling_price_with_tooling = selling_price_with_tooling * exchange_rate.rate

                    result = {
                        'currency': currency,
                        'method': method_name,
                        'order_quantity': total_elements,
                        'cost_production': round(cost_total_production_no_tooling, 3),
                        'cost_material': round(cost_material, 3),
                        'cost_element': round(cost_per_element_no_tooling, 3),
                        'selling_price': round(selling_price_no_tooling, 3),
                        'elements_per_sheet': elements_per_sheet,
                        'num_sheets': num_sheets_needed,
                        'tooling_cost_expressed': tooling_cost_expressed if 'tooling_cost_expressed' in locals() else None,
                        'tooling_cost_distributed': tooling_cost_per_production if tooling_cost > 0 else None,
                        'element_dimension_x': element_dimension_x,
                        'element_dimension_y': element_dimension_y
                    }
                    results.append(result)

        if production_type_choice == 'best':
            best_result = min(results, key=lambda x: x['cost_element']) if results else None
            return render_template('quote_result.html', title='Risultato Preventivo', results=[best_result], quantity_requested=quantity_requested, material=material)
        else:
            return render_template('quote_result.html', title='Risultato Preventivo', results=results, quantity_requested=quantity_requested, material=material)

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

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Utente aggiunto con successo!', 'success')
        return redirect(url_for('user_management'))
    return render_template('admin/add_user.html', title='Aggiungi Utente', form=form)

@app.route('/admin/materials')
@login_required
def material_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    materials = Material.query.all()
    return render_template('admin/material_management.html', materials=materials)

@app.route('/admin/materials/add', methods=['GET', 'POST'])
@login_required
def add_material():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    form = MaterialForm()
    form.category.choices = [(category.id, category.name) for category in ProductCategory.query.all()]
    form.brand.choices = [(brand.id, brand.name) for brand in ProductBrand.query.all()]
    if form.validate_on_submit():
        new_material = Material(name=form.name.data, cost_per_unit=form.cost_per_unit.data,
        unit=form.unit.data, width=form.width.data,
        length=form.length.data, thickness=form.thickness.data,
        currency=form.currency.data,
        brand_id=form.brand.data)
        db.session.add(new_material)
        db.session.commit()
        flash('Materiale aggiunto con successo!', 'success')
        return redirect(url_for('material_management'))
    return render_template('admin/add_material.html', title='Aggiungi Materiale', form=form)

@app.route('/admin/materials/edit/<int:material_id>', methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    material = Material.query.get_or_404(material_id)
    form = MaterialForm(obj=material)
    form.category.choices = [(category.id, category.name) for category in ProductCategory.query.all()]
    form.brand.choices = [(brand.id, brand.name) for brand in ProductBrand.query.all()]
    if form.validate_on_submit():
        material.name = form.name.data
        material.cost_per_unit = form.cost_per_unit.data
        material.unit = form.unit.data
        material.width = form.width.data 
        material.length = form.length.data 
        material.thickness = form.thickness.data
        material.currency = form.currency.data 
        material.category_id = form.category.data
        material.brand_id = form.brand.data
        db.session.commit()
        flash('Materiale modificato con successo!', 'success')
        return redirect(url_for('material_management'))
    return render_template('admin/edit_material.html', title='Modifica Materiale', form=form, material=material)

@app.route('/admin/materials/delete/<int:material_id>', methods=['POST'])
@login_required
def delete_material(material_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Materiale eliminato con successo!', 'success')
    return redirect(url_for('material_management'))

@app.route('/admin/productions')
@login_required
def production_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    productions = Production.query.all()
    return render_template('admin/production_management.html', productions=productions)

@app.route('/admin/productions/add', methods=['GET', 'POST'])
@login_required
def add_production():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    form = ProductionForm()
    if form.validate_on_submit():
        new_production = Production(name=form.name.data, setup_cost=form.setup_cost.data,
        cutting_cost_per_sheet=form.cutting_cost_per_sheet.data)
        db.session.add(new_production)
        db.session.commit()
        flash('Lavorazione aggiunta con successo!', 'success')
        return redirect(url_for('production_management'))
    return render_template('admin/add_production.html', title='Aggiungi Lavorazione', form=form)

@app.route('/admin/productions/edit/<int:production_id>', methods=['GET', 'POST'])
@login_required
def edit_production(production_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    production = Production.query.get_or_404(production_id)
    form = ProductionForm(obj=production)
    if form.validate_on_submit():
        production.name = form.name.data
        production.setup_cost = form.setup_cost.data
        production.cutting_cost_per_sheet = form.cutting_cost_per_sheet.data
        db.session.commit()
        flash('Lavorazione modificata con successo!', 'success')
        return redirect(url_for('production_management'))
    return render_template('admin/edit_production.html', title='Modifica Lavorazione', form=form, production=production)

@app.route('/admin/productions/delete/<int:production_id>', methods=['POST'])
@login_required
def delete_production(production_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    production = Production.query.get_or_404(production_id)
    db.session.delete(production)
    db.session.commit()
    flash('Lavorazione eliminata con successo!', 'success')
    return redirect(url_for('production_management'))

@app.route('/admin/categories')
@login_required
def category_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    categories = ProductCategory.query.all()
    return render_template('admin/category_management.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    form = ProductCategoryForm()
    if form.validate_on_submit():
        new_category = ProductCategory(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash('Categoria aggiunta con successo!', 'success')
        return redirect(url_for('category_management'))
    return render_template('admin/add_category.html', title='Aggiungi Categoria', form=form)

@app.route('/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    category = ProductCategory.query.get_or_404(category_id)
    form = ProductCategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Categoria modificata con successo!', 'success')
        return redirect(url_for('category_management'))
    return render_template('admin/edit_category.html', title='Modifica Categoria', form=form, category=category)

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    category = ProductCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria eliminata con successo!', 'success')
    return redirect(url_for('category_management'))

@app.route('/admin/brands')
@login_required
def brand_management():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    brands = ProductBrand.query.all()
    return render_template('admin/brand_management.html', brands=brands)

@app.route('/admin/brands/add', methods=['GET', 'POST'])
@login_required
def add_brand():
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    form = ProductBrandForm()
    if form.validate_on_submit():
        new_brand = ProductBrand(name=form.name.data)
        db.session.add(new_brand)
        db.session.commit()
        flash('Marca aggiunta con successo!', 'success')
        return redirect(url_for('brand_management'))
    return render_template('admin/add_brand.html', title='Aggiungi Marca', form=form)

@app.route('/admin/brands/edit/<int:brand_id>', methods=['GET', 'POST'])
@login_required
def edit_brand(brand_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    brand = ProductBrand.query.get_or_404(brand_id)
    form = ProductBrandForm(obj=brand)
    if form.validate_on_submit():
        brand.name = form.name.data
        db.session.commit()
        flash('Marca modificata con successo!', 'success')
        return redirect(url_for('brand_management'))
    return render_template('admin/edit_brand.html', title='Modifica Marca', form=form, brand=brand)

@app.route('/admin/brands/delete/<int:brand_id>', methods=['POST'])
@login_required
def delete_brand(brand_id):
    if current_user.role != 'admin':
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('admin_dashboard'))
    brand = ProductBrand.query.get_or_404(brand_id)
    db.session.delete(brand)
    db.session.commit()
    flash('Marca eliminata con successo!', 'success')
    return redirect(url_for('brand_management'))

@app.route('/send_quote_email', methods=['POST'])
@login_required
def send_quote_email():
    material_id = request.form.get('material_id')
    element_dimension_x = request.form.get('element_dimension_x')
    element_dimension_y = request.form.get('element_dimension_y')
    quantity_requested = request.form.get('quantity_requested')
    production_type = request.form.get('production_type')
    recipient_email = request.form.get('email')

    material = Material.query.get(material_id)

    # Crea il corpo dell'email con i dettagli del preventivo
    body = f"Preventivo per {material.brand.name} - {material.category.name} - {material.name}\n\n"
    body += f"Dimensioni elemento: {element_dimension_x}mm x {element_dimension_y}mm\n"
    body += f"Quantitativo richiesto: {quantity_requested}\n"
    body += f"Tipologia di produzione: {production_type}\n\n"

    # Aggiungi i risultati del preventivo al corpo dell'email (assumendo che siano disponibili)
    results = request.form.get('results') # Dovresti passare i risultati dal template, al form.
    if results:
        body += "Risultati del preventivo:\n"
        # Qui dovresti formattare i risultati in modo appropriato
        body += str(results)

    msg = Message("Preventivo Richiesto", recipients=[recipient_email])
    msg.body = body

    try:
        mail.send(msg)
        flash("Preventivo inviato con successo!", "success")
    except Exception as e:
        flash(f"Si è verificato un errore durante l'invio dell'email: {e}", "danger")

    return redirect(url_for('quote'))

@app.route('/admin/settings')
@login_required
def admin_settings():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    settings = Setting.query.all()
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/settings/add', methods=['GET', 'POST'])
@login_required
def add_setting():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    form = SettingForm()
    if form.validate_on_submit():
        setting = Setting(name=form.name.data, value=form.value.data)
        db.session.add(setting)
        db.session.commit()
        flash('Impostazione aggiunta con successo.', 'success')
        return redirect(url_for('admin_settings'))
    return render_template('admin/setting_form.html', form=form, title='Aggiungi Impostazione')

@app.route('/admin/settings/edit/<int:setting_id>', methods=['GET', 'POST'])
@login_required
def edit_setting(setting_id):
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    setting = Setting.query.get_or_404(setting_id)
    form = SettingForm(obj=setting)
    if form.validate_on_submit():
        setting.name = form.name.data
        setting.value = form.value.data
        db.session.commit()
        flash('Impostazione modificata con successo.', 'success')
        return redirect(url_for('admin_settings'))
    return render_template('admin/setting_form.html', form=form, title='Modifica Impostazione')

@app.route('/admin/settings/delete/<int:setting_id>')
@login_required
def delete_setting(setting_id):
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    setting = Setting.query.get_or_404(setting_id)
    db.session.delete(setting)
    db.session.commit()
    flash('Impostazione eliminata con successo.', 'success')
    return redirect(url_for('admin_settings'))

@app.route('/admin/export')
@login_required
def export_data():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    return render_template('admin/export_data.html')

@app.route('/admin/download_data', methods=['POST'])
@login_required
def download_data():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    data_type = request.form.get('data_type')

    if data_type == 'users':
        data = User.query.all()
        header = ['ID', 'Email', 'Role']
        rows = [[user.id, user.email, user.role] for user in data]
    elif data_type == 'materials':
        data = Material.query.all()
        header = ['ID', 'Brand', 'Category', 'Name', 'Width', 'Length', 'Thickness', 'Cost Per Unit']
        rows = [[material.id, material.brand.name, material.category.name, material.name, material.width, material.length, material.thickness, material.cost_per_unit] for material in data]
    elif data_type == 'productions':
        data = Production.query.all()
        header = ['ID', 'Name', 'Setup Cost', 'Cutting Cost Per Sheet']
        rows = [[production.id, production.name, production.setup_cost, production.cutting_cost_per_sheet] for production in data]
    elif data_type == 'quotes':
        data = Quote.query.all()
        header = ['ID', 'User ID', 'Material ID', 'Production ID', 'Quantity', 'Date']
        rows = [[quote.id, quote.user_id, quote.material_id, quote.production_id, quote.quantity, quote.date] for quote in data]
    elif data_type == 'categories':
        data = ProductCategory.query.all()
        header = ['ID', 'Name']
        rows = [[category.id, category.name] for category in data]
    elif data_type == 'brands':
        data = ProductBrand.query.all()
        header = ['ID', 'Name']
        rows = [[brand.id, brand.name] for brand in data]
    elif data_type == 'settings':
        data = Setting.query.all()
        header = ['ID', 'Name', 'Value']
        rows = [[setting.id, setting.name, setting.value] for setting in data]
    else:
        flash('Tipo di dati non valido.', 'danger')
        return redirect(url_for('export_data'))

    output = io.BytesIO()
    writer = csv.writer(io.TextIOWrapper(output, encoding='utf-8'))
    writer.writerow(header)
    writer.writerows(rows)

    output.seek(0)
    csv_data = output.getvalue()
    return send_file(
        io.BytesIO(csv_data),
        as_attachment=True,
        download_name=f'{data_type}.csv',
        mimetype='text/csv'
        )

@app.route('/admin/exchange_rates')
@login_required
def admin_exchange_rates():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    exchange_rates = ExchangeRate.query.all()
    return render_template('admin/exchange_rates.html', exchange_rates=exchange_rates)

@app.route('/admin/exchange_rates/add', methods=['GET', 'POST'])
@login_required
def add_exchange_rate():
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    form = ExchangeRateForm()
    if form.validate_on_submit():
        exchange_rate = ExchangeRate(
            currency=form.currency.data.upper(),
            rate=form.rate.data
        )
        db.session.add(exchange_rate)
        db.session.commit()
        flash('Tasso di cambio aggiunto con successo.', 'success')
        return redirect(url_for('admin_exchange_rates'))
    return render_template('admin/edit_exchange_rate.html', form=form, title='Aggiungi Tasso di Cambio', exchange_rate=None)

@app.route('/admin/exchange_rates/edit/<int:exchange_rate_id>', methods=['GET', 'POST'])
@login_required
def edit_exchange_rate(exchange_rate_id):
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    exchange_rate = ExchangeRate.query.get_or_404(exchange_rate_id)
    form = ExchangeRateForm(obj=exchange_rate)
    if form.validate_on_submit():
        exchange_rate.currency = form.currency.data.upper()
        exchange_rate.rate = form.rate.data
        db.session.commit()
        flash('Tasso di cambio modificato con successo.', 'success')
        return redirect(url_for('admin_exchange_rates'))
    return render_template('admin/edit_exchange_rate.html', form=form, title='Modifica Tasso di Cambio', exchange_rate=exchange_rate)

@app.route('/admin/exchange_rates/delete/<int:exchange_rate_id>')
@login_required
def delete_exchange_rate(exchange_rate_id):
    if current_user.role != 'admin':
        flash('Non hai i permessi per accedere a questa pagina.', 'danger')
        return redirect(url_for('index'))

    exchange_rate = ExchangeRate.query.get_or_404(exchange_rate_id)
    db.session.delete(exchange_rate)
    db.session.commit()
    flash('Tasso di cambio eliminato con successo.', 'success')
    return redirect(url_for('admin_exchange_rates'))