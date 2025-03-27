from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DecimalField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ricordami')
    submit = SubmitField('Accedi')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password', message='Le password devono corrispondere.')])
    submit = SubmitField('Registrati')

class QuoteForm(FlaskForm):
    material_type = SelectField('Tipologia Materiale', validators=[DataRequired()], coerce=int)
    max_dimension = StringField('Dimensioni Massime Elemento', validators=[DataRequired()])
    quantity = IntegerField('Quantitativo Richiesto', validators=[DataRequired()])
    drawing = FileField('Disegno (PDF/DXF)')
    production_type = SelectField('Tipologia Produzione', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Calcola Preventivo')

class MaterialForm(FlaskForm):
    name = StringField('Nome Materiale', validators=[DataRequired()])
    cost_per_unit = DecimalField('Costo per Unità', validators=[DataRequired()])
    unit = StringField('Unità', validators=[DataRequired()])
    width = DecimalField('Larghezza (mm)', validators=[DataRequired()])
    length = DecimalField('Lunghezza (mm)', validators=[DataRequired()])
    thickness = DecimalField('Spessore (mm)')
    currency = SelectField('Valuta', choices=[('EUR', 'Euro'), ('USD', 'Dollaro USA'), ('CNY', 'Yuan Cinese'), ('Altro', 'Altro')])
    category = SelectField('Categoria Prodotto', validators=[DataRequired()], coerce=int)
    brand = SelectField('Marca Prodotto', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Salva Materiale')

class ProductionForm(FlaskForm):
    name = StringField('Nome Lavorazione', validators=[DataRequired()])
    setup_cost = DecimalField('Costo Setup', validators=[DataRequired()])
    cutting_cost_per_sheet = DecimalField('Costo Taglio per Lastra', validators=[DataRequired()])
    submit = SubmitField('Salva Lavorazione')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Ruolo', choices=[('user', 'Utente'), ('admin', 'Amministratore')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Salva Utente')