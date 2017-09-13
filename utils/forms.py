from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, TextAreaField
from wtforms.widgets import TextArea
from flask_pagedown.fields import PageDownField
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


class AddNoteForm(FlaskForm):
    note_title = TextField('Note Title:', [validators.Required("Please enter \
      your name.")])
    # note = TextAreaField('Note:', [validators.Required("Please enter \
    #   your password.")], widget=TextArea())
    note = PageDownField('Your Note:')
    submit = SubmitField('Add Note')
