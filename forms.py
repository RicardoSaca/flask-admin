from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField,SubmitField, validators

class SigninForm(FlaskForm):
    name = StringField("Name",  [validators.Length(min=4, max=25)])
    password = PasswordField("Password",  [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    name = StringField("Name",  [validators.Length(min=4, max=25)])
    password = PasswordField("Password",  [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField("Submit")