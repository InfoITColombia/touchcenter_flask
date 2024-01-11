from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, SelectField, PasswordField, IntegerField, FileField, DateField, EmailField, DecimalField, HiddenField


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
    n_proveedor = StringField('Proveedor', id='n_proveedor', validators=[DataRequired()])
    #k_proveedor = HiddenField('IdProveedor')

class newProveedorForm(FlaskForm):
    n_proveedor = StringField('Nombre', validators=[DataRequired()])
    dir_proveedor = StringField('Dirección', validators=[DataRequired()])
    tel_proveedor = StringField('Teléfono', validators=[DataRequired()])

class newClienteForm(FlaskForm):
    id_cliente =StringField('ID', validators=[DataRequired()])
    n_cliente = StringField('Nombre', validators=[DataRequired()])
    tel_cliente = StringField('Telefono', validators=[DataRequired()])
    email_cliente = EmailField('E-Mail', validators=[DataRequired()])

class newServicioForm(FlaskForm):
    n_servicio = StringField('Nombre servicio', validators=[DataRequired()])
    desc_servicio = StringField('Descripción servicio', validators=[DataRequired()])
    #v_agregado = DecimalField(places=2, validators=[DataRequired()])

class newVentaForm(FlaskForm):
    #k_cliente = StringField('Nombre servicio', validators=[DataRequired()])
    k_servicio = StringField('Servicio ', validators=[DataRequired()])
    k_producto = StringField('Nombre producto ', id="k_producto", validators=[DataRequired()])
    q_item = IntegerField('Cantidad ', validators=[DataRequired()])
