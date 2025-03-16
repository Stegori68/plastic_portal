import requests
from datetime import datetime

@celery.task
def update_currency_rates():
    app = create_app()
    with app.app_context():
        response = requests.get(
            f"https://api.forexrateapi.com/v1/latest?api_key={app.config['CURRENCY_API_KEY']}&base=EUR"
        )
        rates = response.json()['rates']
        
        for currency in ['USD', 'CNY']:
            rate = CurrencyRate(
                base_currency='EUR',
                target_currency=currency,
                rate=rates[currency],
                date=datetime.utcnow()
            )
            db.session.add(rate)
        db.session.commit()