from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

boulder_levels = [('0', 'N/A'),
        ('1', 'V1'),
        ('2', 'V2'),
        ('3', 'V3'),
        ('4', 'V4'),
        ('5', 'V5'),
        ('6', 'V6'),
        ('7', 'V7'),
        ('8', 'V8+')]

sport_levels = [('0', 'N/A'),
        ('1', '5.9'),
        ('2', '5.10a-b'),
        ('3', '5.10c-d'),
        ('4', '5.11a-b'),
        ('5', '5.11c-d'),
        ('6', '5.12a-b'),
        ('7', '5.12c-d'),
        ('8', '5.13a-b'),
        ('9', '5.13c-d'),
        ('10', '5.14+')]

class EditProfileForm(FlaskForm):
    """For editing the profile for a user"""

    img_url = StringField('Profile Picture', validators=[]) #File Upload field?
    username = StringField('Username', validators=[])
    email = StringField('E-mail', validators=[])
    b_skill_level = SelectField('Boulder Skill Level', choices=[(id, value) for (id, value) in boulder_levels])
    tr_skill_level = SelectField('Top Rope Skill Level', choices=[(id, value) for (id, value) in sport_levels])
    ld_skill_level = SelectField('Lead Climbing Skill Level', choices=[(id, value) for (id,value) in sport_levels])
    goals = TextAreaField('Your Climbing Goals', validators=[])
    location = StringField('Your Location', validators=[])

class EditClimbInfo(FlaskForm):
    """Quick edit of user goals"""
    b_skill_level = SelectField('Boulder Skill Level', choices=[(id, value) for (id, value) in boulder_levels])
    tr_skill_level = SelectField('Top Rope Skill Level', choices=[(id, value) for (id, value) in sport_levels])
    ld_skill_level = SelectField('Lead Climbing Skill Level', choices=[(id, value) for (id,value) in sport_levels])
    goals = TextAreaField('Your Climbing Goals', validators=[])