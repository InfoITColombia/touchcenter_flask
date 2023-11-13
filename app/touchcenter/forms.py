from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, SelectField, PasswordField, IntegerField, FileField, DateField, EmailField, DecimalField


class LoginUsuarioForm(FlaskForm):
    usuario =  StringField('Usuario', validators=[DataRequired()])
    pwd_usuario =  PasswordField('Contraseña', validators=[DataRequired()])

class RegistroUsuarioForm(FlaskForm):
    usuario =  StringField('Usuario', validators=[DataRequired()])
    pwd_usuario =  PasswordField('Contraseña', validators=[DataRequired()])

class newClienteForm(FlaskForm):
    id_cliente = StringField('Identificación', validators=[DataRequired()])
    n_cliente = StringField('Nombre cliente', validators=[DataRequired()])
    tel_cliente = StringField('Teléfono', validators=[DataRequired()])
    email_cliente = EmailField('E-mail', validators=[DataRequired()])

class newArticuloForm(FlaskForm):
    n_articulo = StringField('Nombre', validators=[DataRequired()])
    desc_articulo = StringField('Descricpión', validators=[DataRequired()])
    v_articulo = DecimalField(places=2,  validators=[DataRequired()])
    q_articulo = IntegerField('Cantidad', validators=[DataRequired()])
    k_proveedor = StringField('Proveedor', id='k_proveedor', validators=[DataRequired()])

class newProveedorForm(FlaskForm):
    n_proveedor = StringField('Nombre', validators=[DataRequired()])
    dir_proveedor = StringField('Dirección', validators=[DataRequired()])
    tel_proveedor = StringField('Teléfono', validators=[DataRequired()])
   