from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from lib.util_wtforms import ModelForm
from funandprofit.blueprints.user.models import User, db
from funandprofit.blueprints.user.validations import ensure_identity_exists, \
    ensure_existing_password_matches

from wtforms_components import EmailField, Email, Unique

class LoginForm(Form):
    next = HiddenField()
    studentname = StringField('Student First Name',
                           [DataRequired(), Length(3, 254)])
    studentnumber = IntegerField('Student Number',
                                 [DataRequired()])
    studentemail = EmailField('Student Email',validators=[
        DataRequired(),
        Email(),
        Length(3, 254)])
    ##password = PasswordField('Password', [DataRequired(), Length(8, 128)])
    # remember = BooleanField('Stay signed in')


class BeginPasswordResetForm(Form):
    identity = StringField('Username or email',
                           [DataRequired(),
                            Length(3, 254),
                            ensure_identity_exists])


class PasswordResetForm(Form):
    reset_token = HiddenField()
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


class SignupForm(ModelForm):
    '''
    email = EmailField(validators=[
        DataRequired(),
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])
    '''
    first_name = StringField('Student First Name',
                             [DataRequired(), Length(3, 254)])
    student_number = IntegerField('Student Number',
                                  [DataRequired()])
    email = EmailField(validators=[
        DataRequired(),
        Email(),
        Length(3, 254)])
    money = IntegerField('Student Money',
                         [DataRequired()])


class WelcomeForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    first_name = StringField(validators=[
        Unique(
            User.email,
            get_session=lambda: db.session
        ),
        DataRequired(),
        Length(1, 16),
        Regexp('^\w+$', message=username_message)
    ])


class UpdateCredentials(ModelForm):
    current_password = PasswordField('Current password',
                                     [DataRequired(),
                                      Length(8, 128),
                                      ensure_existing_password_matches])

    email = EmailField(validators=[
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('Password', [Optional(), Length(8, 128)])
