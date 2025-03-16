import click
from flask import current_app, cli
from flask_migrate import Migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("seed-db")
def seed_db():
    """Popola il database con dati demo"""
    from werkzeug.security import generate_password_hash
    
    # Utenti
    admin = User(
        email='gori@weltelectronic.it',
        password_hash=generate_password_hash('Admin123!'),
        role='admin'
    )
    
    user = User(
        email='stegori@tiscali.it',
        password_hash=generate_password_hash('User123!'),
        role='user'
    )
    
    # Materiali
    materials = [
        Material(
            name="PVC 3mm Standard",
            thickness=3.0,
            cost=45.0,
            width=2000,
            height=1000
        ),
        Material(
            name="Policarbonato 5mm",
            thickness=5.0,
            cost=68.0,
            width=2500,
            height=1250
        )
    ]
    
    # Tipologie lavorazione
    production_types = [
        ProductionType(
            name="Taglio passante a fustella testa piana",
            setup_cost=150.0,
            cutting_cost=2.5
        ),
        ProductionType(
            name="Mezzo taglio a rotativa",
            setup_cost=80.0,
            cutting_cost=1.8
        )
    ]
    
    try:
        db.session.add_all([admin, user] + materials + production_types)
        db.session.commit()
        print("Database popolato con successo!")
    except Exception as e:
        db.session.rollback()
        print(f"Errore: {str(e)}")