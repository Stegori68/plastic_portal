from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

class UserAdminView(ModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    
    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            model.password_hash = generate_password_hash(form.password.data)

def configure_admin(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=SecureAdminIndexView())
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ModelView(Material, db.session))
    admin.add_view(ModelView(ProductionType, db.session))
    admin.add_view(ModelView(CurrencyRate, db.session))

class ProductionTypeAdmin(ModelView):
    form_choices = {
        'category': [
            ('plotter', 'Plotter'),
            ('fustella', 'Fustella')
        ]
    }
    
    form_args = {
        'tooling_cost': {
            'validators': [Optional()],
            'render_kw': {
                'data-bs-toggle': 'tooltip', 
                'title': 'Inserire solo per produzione a fustella'
            }
        }
    }
    
    def on_form_prefill(self, form, id):
        if form.category.data == 'plotter':
            form.tooling_cost.render_kw = {'disabled': True}