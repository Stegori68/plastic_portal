from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DecimalField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, ValidationError

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
    element_dimension_x = DecimalField('Dimensione Massima Elemento X (mm)', validators=[DataRequired(), NumberRange(min=0)])
    element_dimension_y = DecimalField('Dimensione Massima Elemento Y (mm)', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantitativo Richiesto', validators=[DataRequired(), NumberRange(min=1)])
    drawing = FileField('Disegno (PDF/DXF)')
    production_type = SelectField('Tipologia Produzione', validators=[DataRequired()])
    fustella_productions = IntegerField('Numero di Produzioni per Ammortizzare la Fustella', validators=[NumberRange(min=1)], default=4)
    submit = SubmitField('Calcola Preventivo')

    def validate_drawing(form, field):
        if field.data:
            if not field.data.filename.lower().endswith(('.pdf', '.dxf')):
                raise ValidationError('Formato file non valido. Si prega di caricare un file PDF o DXF.')

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

class ProductCategoryForm(FlaskForm):
    name = StringField('Nome Categoria', validators=[DataRequired()])
    submit = SubmitField('Salva Categoria')

class ProductBrandForm(FlaskForm):
    name = StringField('Nome Marca', validators=[DataRequired()])
    submit = SubmitField('Salva Marca')

class SettingForm(FlaskForm):
    name = StringField('Nome Impostazione', validators=[DataRequired()])
    value = StringField('Valore', validators=[DataRequired()])
    submit = SubmitField('Salva Impostazione')
    