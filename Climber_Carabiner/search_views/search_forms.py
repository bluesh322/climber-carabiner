from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SearchForm(FlaskForm):
    q = StringField('q', validators=[])