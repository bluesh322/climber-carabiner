from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserSignupForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat password', validators=[Length(min=6)])

class UserLoginForm(FlaskForm):
    """For for logging in a user"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    
class ForgetPasswordForm(FlaskForm):
    """For sending confirmation email to change password"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])

class ChangePasswordForm(FlaskForm):
    """For changing the password for a user whose confirmed their email"""

    password = PasswordField('Password', validators=[Length(min=6), DataRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat password', validators=[Length(min=6)])