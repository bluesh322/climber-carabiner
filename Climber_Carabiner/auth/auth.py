from flask import current_app, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from flask_mail import Message
from ..models import User, db
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import datetime

sess = db.session

s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates', 
    static_folder='static'
)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('rememeber') else False

    user = User.authenticate(email, password)
    if not user.confirmed:
        flash("Your email has not yet been confrimed, check your email for confirmation")
        return redirect(url_for('auth_bp.login'))
    if not user:
        flash("Your email or password do not match our records")
        return redirect(url_for('auth_bp.login'))
    login_user(user, remember=remember)
    return redirect(url_for('index_bp.show_profile'))

@auth_bp.route('/signup')
def signup():
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def add_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists.")
        return redirect(url_for('auth_bp.login'))
    
    new_user = User.signup(username=username, email=email, password=password)
    sess.commit()

    token = generate_confirmation_token(new_user.email)
    confirm_url = url_for('auth_bp.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Confirmation Email from Climber Carabiner"
    send_email(new_user.email, subject, html)
    flash('A confirmation email has been sent via email.', 'success')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
def logout():
    return redirect(url_for('index.index'))

@auth_bp.route('/emailverify')
def verify_email():
    email = 'koheji2761@mailetk.com'
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirmation Email', sender='bluesh322@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)

    msg.body = f'Your link is {link}'

    mail.send(msg)

    return render_template(url_for('index.index'), token=token)

@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or expired', 'danger')
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        sess.add(user)
        sess.commit()
        flash('Your account confirmation is complete!', 'success')
    return redirect(url_for('auth_bp.login'))