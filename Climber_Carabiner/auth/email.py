from flask_mail import Message
from flask import current_app

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_USERNAME']
    )
    mail = current_app.extensions.get('mail')
    mail.send(msg)