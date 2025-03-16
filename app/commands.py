# app/commands.py
import click
from flask import current_app, cli
from flask_migrate import Migrate
from app import create_app, db
from datetime import datetime
from models import User

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("seed-db")
def seed_db():
    """Popola il database con dati demo"""
    
    # Utenti
    admin = User(
        email='gori@weltelectronic.it',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    
    user = User(
        email='stegori@tiscali.it',
        password_hash=generate_password_hash('user123'),
        role='user'
    )
    
    # Materiali
    materials = [
        Material(
            name="PVC Rigido 3mm",
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
            name="Taglio passante a plotter",
            category="plotter",
            setup_cost=40.0,
            cutting_cost=7.0,
            tooling_cost=None
        ),
        ProductionType(
            name="Mezzo taglio a plotter",
            category="plotter",
            setup_cost=40.0,
            cutting_cost=7.0,
            tooling_cost=None
        ),
        ProductionType(
            name="Taglio passante a fustella testa piana",
            category="fustella",
            setup_cost=20.0,
            cutting_cost=4.0,
            tooling_cost=300.0
        ),
        ProductionType(
            name="Mezzo taglio a fustella testa piana",
            category="fustella",
            setup_cost=20.0,
            cutting_cost=4.0,
            tooling_cost=300.0
        )
    ]
    
    db.session.add_all([admin, user] + materials + production_types)
    db.session.commit()