#from app.db import db, ma
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from db import db, ma
from datetime import datetime
from base64 import b64encode


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    n_proveedor = db.Column(db.String(100), nullable = False)
    dir_proveedor = db.Column(db.String(50))
    tel_proveedor = db.Column(db.String(50))

class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    n_articulo = db.Column(db.String(100), nullable = False)
    desc_articulo = db.Column(db.String(300))
    v_articulo = db.Column(db.Column(db.Numeric(11,2), nullable = False ))
    q_Articulo = db.Column(db.Integer)
    #Llaves foráneas
    k_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id") ,primary_key=True)
    #atributos de la relacion
    proveedor = db.relationship("Proveedor")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    k_articulo = db.Column(db.Integer, db.ForeignKey("articulo.id"),primary_key=True)
    k_venta =db.Column(db.Integer, db.ForeignKey("venta.id"), primary_key=True)
    q_item = db.Column(db.Integer)
    vu_item = db.Column(db.Column(db.Numeric(11,2), nullable = False ))
    #atributos de la relacion
    articulo = db.relationship("Articulo")
    venta = db.relationship("Venta")

class Venta(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    k_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id") ,primary_key=True)
    k_usuario = db.Column(db.String(20), db.ForeignKey("usuario.n_usuario"), primary_key=True)
    f_venta = db.Column(db.DateTime, default= datetime.now())
    v_total_venta = db.Column(db.Column(db.Numeric(11,2), nullable = False ))
    #atributos de la relacion
    cliente = db.relationship("Cliente")
    usuario = db.relationship("Usuario")

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente =db.Column(db.String(20), nullable = False) 
    n_cliente = db.Column(db.String(100), nullable = False)
    tel_cliente = db.Column(db.String(20))
    email_cliente = db.Column(db.String(30))

class Usuario (db.Model):
    n_usuario = db.Column(db.String(20), primary_key=True)
    pwd_usuario = db.Column(db.String(100), nullable = False)

