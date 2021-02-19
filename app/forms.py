from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms import DataRequired, Form, BooleanField, StringField, PasswordField, SubmitField, validators


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', [validators.Length(min=5, max=10)])
    password = PasswordField('Contraseña',[validators.DataRequired()])
    submit = SubmitField('Enviar')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', [validators.Length(min=4, max=25)])
    password = PasswordField('Contraseña', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirmar contraseña')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Registrar')