#from app.db import db, ma
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from ..database import db, ma
from datetime import datetime
from base64 import b64encode


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    n_proveedor = db.Column(db.String(100), nullable = False)
    dir_proveedor = db.Column(db.String(50))
    tel_proveedor = db.Column(db.String(50))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    n_articulo = db.Column(db.String(100), nullable = False)
    desc_articulo = db.Column(db.String(300))
    v_articulo = db.Column(db.Numeric(11,2), nullable = False )
    q_Articulo = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #Llaves foráneas
    k_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id") ,primary_key=True)
    #atributos de la relacion
    proveedor = db.relationship("Proveedor")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    k_articulo = db.Column(db.Integer, db.ForeignKey("articulo.id"),primary_key=True)
    k_venta =db.Column(db.Integer, db.ForeignKey("venta.id"), primary_key=True)
    q_item = db.Column(db.Integer)
    vu_item = db.Column(db.Numeric(11,2), nullable = False )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #atributos de la relacion
    articulo = db.relationship("Articulo")
    venta = db.relationship("Venta")

class Venta(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    k_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id") ,primary_key=True)
    k_usuario = db.Column(db.String(20), db.ForeignKey("usuario.n_usuario"), primary_key=True)
    f_venta = db.Column(db.DateTime, default= datetime.now())
    v_total_venta = db.Column(db.Numeric(11,2), nullable = False )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #atributos de la relacion
    cliente = db.relationship("Cliente")
    usuario = db.relationship("Usuario")

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente =db.Column(db.String(20), nullable = False) 
    n_cliente = db.Column(db.String(100), nullable = False)
    tel_cliente = db.Column(db.String(20))
    email_cliente = db.Column(db.String(30))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Usuario (db.Model):
    n_usuario = db.Column(db.String(20), primary_key=True)
    pwd_usuario = db.Column(db.String(100), nullable = False)
    tipo_usuario = db.Column(db.String(20), nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

#ESQUEMAS schema
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        fields = ["n_usuario", "pwd_usuario"]



def get_user_by_usuario(usuario):
    usuario_qs = Usuario.query.filter_by(n_usuario = usuario).first()
    usuario_schema = UsuarioSchema()
    u = usuario_schema.dump(usuario_qs)
    return u


def register_user(usuario, pwd, tipo):
    usuario = Usuario(n_usuario = usuario,pwd_usuario=pwd, tipo_usuario = tipo)
    try:
        db.session.add(usuario)
        db.session.commit()
        return usuario.n_usuario
    except Exception as e:
        print ("No se registró el ususario "+ str(e))
        return None     

def register_proveedor(nombre,dir, tel):
    proveedor = Proveedor(n_proveedor = nombre, dir_proveedor = dir, tel_proveedor = tel)
    try:
        db.session.add(proveedor)
        db.session.commit()
        return proveedor
    except Exception as e:
        print ("No se registró el proveedor "+ str(e))
        return None 

def get_proveedores():
    proveedores = Proveedor.query.all()
    print(proveedores)
    return Proveedor.query.all()

def register_articulo(n_articulo, desc_articulo, v_articulo,q_Articulo, k_proveedor):
    articulo = Articulo(n_articulo = n_articulo, desc_articulo = desc_articulo, v_articulo = v_articulo,q_Articulo = q_Articulo, k_proveedor=k_proveedor)
    try:
        db.session.add(articulo)
        db.session.commit()
        return articulo
    except Exception as e:
        print ("No se registró el proveedor "+ str(e))
        return None    
    