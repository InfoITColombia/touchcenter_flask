from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, SelectField, PasswordField, IntegerField, FileField, DateField


class LoginUsuarioForm(FlaskForm):
    email_usuario =  StringField('Email', validators=[DataRequired()])
    pwd_usuario =  PasswordField('Contraseña', validators=[DataRequired()])