from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, SelectField, FileField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Email, Length, EqualTo

boulder_levels = [ 'V','V0',
         'V1',
         'V2',
         'V3',
         'V4',
         'V5',
         'V6',
         'V7',
         'V8',
         'V9']

sport_levels = ['5.4','5.5', '5.6',
        '5.6+',
        '5.7-',
        '5.7',
        '5.7+',
        '5.8-',
        '5.8',
        '5.8+',
        '5.9-',
        '5.9',
        '5.9+',
        '5.10',
        '5.10a',
        '5.10b',
        '5.10c',
        '5.10d',
        '5.11',
        '5.11a',
        '5.11b',
        '5.11c',
        '5.11d',
        '5.12',
        '5.12a',
        '5.12b',
        '5.12c',
        '5.12d',
        '5.13',
        '5.13a',
        '5.13b',
        '5.13c',
        '5.13d',
        '5.14',
        '5.14a',
        '5.14b']

class EditProfileForm(FlaskForm):
    """For editing the profile for a user"""

    img_url = StringField('Profile Picture', validators=[]) #File Upload field?
    username = StringField('Username', validators=[])
    email = StringField('E-mail', validators=[])
    b_skill_level = SelectField('Boulder Skill Level', choices=[(id, value) for (id, value) in list(enumerate(boulder_levels))], coerce=int, validators=[])
    tr_skill_level = SelectField('Top Rope Skill Level', choices=[(id, value) for (id, value) in list(enumerate(sport_levels))], coerce=int, validators=[])
    ld_skill_level = SelectField('Lead Climbing Skill Level', choices=[(id, value) for (id,value) in list(enumerate(sport_levels))], coerce=int, validators=[])
    goals = TextAreaField('Your Climbing Goals', validators=[])
    location = StringField('Your Location', validators=[])

class EditClimbInfo(FlaskForm):
    """Quick edit of user goals"""
    b_skill_level = SelectField('Boulder Skill Level', choices=[(id, value) for (id, value) in list(enumerate(boulder_levels))], coerce=int, validators=[])
    tr_skill_level = SelectField('Top Rope Skill Level', choices=[(id, value) for (id, value) in list(enumerate(sport_levels))], coerce=int, validators=[])
    ld_skill_level = SelectField('Lead Climbing Skill Level', choices=[(id, value) for (id,value) in list(enumerate(sport_levels))], coerce=int, validators=[])
    goals = TextAreaField('Your Climbing Goals', validators=[])