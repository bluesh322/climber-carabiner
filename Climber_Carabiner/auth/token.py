from itsdangerous import URLSafeTimedSerializer

from flask import current_app

def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=60):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(
            token,
            salt='email-confirm',
            max_age=expiration
        )
    except:
        return False
    return email