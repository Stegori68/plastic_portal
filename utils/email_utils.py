from flask_mail import Message
from plastic_portal import app, mail

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_quote_email(quote, recipient_email):
    # ... (Logica per generare il contenuto dell'email del preventivo) ...
    send_email(f"Preventivo N. {quote.id}", [recipient_email], "Testo del preventivo...", "HTML del preventivo...")