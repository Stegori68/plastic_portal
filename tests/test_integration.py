import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Crea utente test
        user = User(email='test@example.com', password_hash='test123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_full_flow(self):
        # Login
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Nuova quotazione
        response = self.client.get(url_for('main.new_quote'))
        self.assertIn(b"Nuova Quotazione", response.data)