from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, InputRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class RegisterHostel(FlaskForm):
    hs_name = StringField('Hostel Name')
    hs_address = StringField('Hostel Address')
    hs_contact = IntegerField('Contact')
    hs_rent = IntegerField('Rent')
    hs_description = StringField('Description')
    rooms = IntegerField('No. of rooms')
    caution = IntegerField('Caution')
    curfew = StringField('Curfew')
    maps_link = StringField('Maps Link')
    type = SelectField('Choose the hostel type', [ InputRequired()], choices=[ ('girls', 'Girls'),('boys', 'Boys') ])
    submit = SubmitField('Add Hostel')