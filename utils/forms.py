from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    username = TextField('Username:', [validators.Required("Please enter \
      your name.")])
    password = PasswordField('Password:', [validators.Required("Please enter \
      your password.")])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = TextField('Username:', [validators.Required("Please enter \
      your name")])
    email = TextField('Email:', [validators.Required("Please enter \
      your email")])
    password = PasswordField('Password:', [validators.Required("Please enter \
      your password"), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password:', [validators.Required("Please enter \
      your password")])
    submit = SubmitField('Signup')
