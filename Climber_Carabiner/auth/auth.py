from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from ..models import User, db

sess = db.session

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
        return redirect(url_for('auth_bp.signup'))
    
    new_user = User.signup(username=username, email=email, password=password)
    sess.commit()
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
def logout():
    return redirect(url_for('index.index'))