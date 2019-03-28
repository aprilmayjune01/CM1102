from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,8}$',
                              message='Your password should be between 6 and 8 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Oh no! This username has already been taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if user:
            raise ValidationError('Oh no! This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    choices = [('Rose', 'Rose'), ('Lily', 'Lily'), ('Daisy', 'Daisy'), ('Sunflower', 'Sunflower'), ('Carnation', 'Carnation'), ('Freesia', 'Freesia'), ('Jasmine', 'Jasmine'), ('Peony', 'Peony'), ('Amaryllis', 'Amaryllis')]
    select = SelectField('Search flower:', choices=choices)
    search = StringField('')

class CheckoutForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired('Please enter your forename'), Length(min=3, max=15)])
    surname = StringField('Surname', validators=[DataRequired('Please enter your surname'), Length(min=3, max=15)])
    address = StringField('Address',
                        validators=[DataRequired('Please enter your billing address')])
    card_no = PasswordField('card_no', validators=[DataRequired('Please enter your 16-digit card number'), Length(min=16, max=16)])
    cvc = PasswordField('cvc', validators=[DataRequired('Please enter your 3-digit CVC'), Length(min=3, max=3)])
    submit = SubmitField('Checkout')




