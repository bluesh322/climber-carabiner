from flask import (
    current_app,
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session
)
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from .auth_forms import UserSignupForm, UserLoginForm, ForgetPasswordForm, ChangePasswordForm
from ..models import User, db
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import datetime

sess = db.session

@current_app.login_manager.user_loader
def load_user(id):
    return User.query.get_or_404(int(id))

@current_app.login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('index_bp.index'))

s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login")
def login():
    form = UserLoginForm()
    return render_template("login.html", form=form)


@auth_bp.route("/login", methods=["POST"])
def login_post():
    form = UserLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #remember = True if request.form.get("rememeber") else False

        user = User.authenticate(email, password)
        if not user:
            flash("Your email or password do not match our records")
            return redirect(url_for("auth_bp.login"))
        if not user.confirmed:
            flash(
                "Your email has not yet been confrimed, check your email for confirmation"
            )
            return redirect(url_for("auth_bp.login"))
        login_user(user)
    return redirect(url_for("user_views.is_user_location"))


@auth_bp.route("/signup")
def signup():
    form = UserSignupForm()
    return render_template("signup.html", form=form)


@auth_bp.route("/signup", methods=["POST"])
def add_user():
    form = UserSignupForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists.")
            return redirect(url_for("auth_bp.login"))
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already taken.")
            return redirect(url_for("auth_bp.signup"))
        new_user = User.signup(username=username, email=email, password=password)
        if new_user == False:
            return redirect(url_for('index_bp.index'))
        sess.commit()
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for("auth_bp.confirm_email", token=token, _external=True)
        html = render_template("activate.html", confirm_url=confirm_url)
        subject = "Confirmation Email from Climber Carabiner"
        send_email(new_user.email, subject, html)
        return redirect(url_for("auth_bp.show_confirm_modal"))
    else:
        return render_template('signup.html', form=form)

@auth_bp.route("/confirm_email", methods=["GET"])
def show_confirm_modal():
    return render_template("confirm_email.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("index_bp.index"))

@auth_bp.route("/reset_password", methods=["GET", "POST"])
def forget_password_form():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email is not registered with us, please sign up or try a different email")
            return redirect(url_for("auth_bp.forget_password_form"))
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("auth_bp.confirm_email_password", token=token, _external=True)
        html = render_template("reset.html", confirm_url=confirm_url)
        subject = "Account Update from Climber Carabiner"
        send_email(user.email, subject, html)
        flash("An email was sent to confirm changing the password", "success")
        return redirect(url_for("auth_bp.login"))
    else:
        return render_template('reset_password.html', form=form)

@auth_bp.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or expired", "danger")
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        sess.add(user)
        sess.commit()
        flash("Your account confirmation is complete!", "success")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/confirm_email_password/<token>")
def confirm_email_password(token):
    try:
        email = confirm_token(token)
    except:
        flask("The confirmation link is invalid or expired", "danger")
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        return redirect(url_for("auth_bp.change_password", email=user.email, token=token))
    else:
        flash("User is not yet confirmed, please confirm your email")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/change_password/<email>&<token>", methods=["GET", "POST"])
def change_password(email, token):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password=form.password.data
        user = User.change_password(email, password)
        if user:
            flash("You have successfully changed your password, please log-in")
        return redirect(url_for("auth_bp.login"))
    else:
        return render_template("change_password.html", form=form)
