#from app.db import db, ma
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from ..database import db, ma
from datetime import datetime, timedelta
from base64 import b64encode


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    n_proveedor = db.Column(db.String(100), nullable = False)
    dir_proveedor = db.Column(db.String(50))
    tel_proveedor = db.Column(db.String(50))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #atributos de la relacion
    #articulos = db.relationship('Articulo', backref='proveedor', lazy=True)

class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n_articulo = db.Column(db.String(100), nullable = False)
    desc_articulo = db.Column(db.String(300))
    v_articulo = db.Column(db.Numeric(11,2), nullable = False )
    q_Articulo = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #Llaves foráneas
    k_proveedor = db.Column(db.Integer, db.ForeignKey("proveedor.id"))
    #atributos de la relacion
    proveedor= db.relationship('Proveedor')
 

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n_servicio = db.Column(db.String(100), nullable = False)
    desc_servicio = db.Column(db.String(300))
    e_servicio = db.Column(db.String(20), nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

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

class Venta(db.Model):
    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    k_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id") )
    k_usuario = db.Column(db.String(20), db.ForeignKey("usuario.n_usuario"))
    f_venta = db.Column(db.DateTime, default= datetime.now())
    v_total_venta = db.Column(db.Numeric(11,2), nullable = False )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #atributos de la relacion
    cliente = db.relationship("Cliente")
    usuario = db.relationship("Usuario")

class Servicio_Venta(db.Model):
    k_venta = db.Column(db.Integer, db.ForeignKey("venta.id") ,primary_key=True)
    k_servicio = db.Column(db.Integer, db.ForeignKey("servicio.id") ,primary_key=True)
    v_agregado = db.Column(db.Numeric(11,2), nullable = False )
    #atributos de la relacion
    venta = db.relationship("Venta")
    servicio = db.relationship("Servicio")

class Item(db.Model):
    k_venta = db.Column(db.Integer, db.ForeignKey("venta.id") ,primary_key=True)
    k_servicio = db.Column(db.Integer, db.ForeignKey("servicio.id") ,primary_key=True)
    k_articulo = db.Column(db.Integer, db.ForeignKey("articulo.id"),primary_key=True)
    q_item = db.Column(db.Integer)
    vu_item = db.Column(db.Numeric(11,2), nullable = False )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    #atributos de la relacion
    articulo = db.relationship("Articulo")
    venta = db.relationship("Venta")
    servicio = db.relationship("Servicio")






#ESQUEMAS schema
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        fields = ["n_usuario", "pwd_usuario"]

class ServicioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio
        fields = ["id", "n_servicio"]

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model : Item
        fields = ["k_venta", "k_servicio", "k_articulo" , "q_item" , "vu_item", "articulo"]

class ArticuloSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model : Articulo
        fields = ["id", "n_articulo", "desc_articulo", "v_articulo", "q_articulo"]



def get_user_by_usuario(usuario):
    usuario_qs = Usuario.query.filter_by(n_usuario = usuario).first()
    usuario_schema = UsuarioSchema()
    u = usuario_schema.dump(usuario_qs)
    return u

def get_proveedores():
    return Proveedor.query.all()


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


def get_servicios():
    servicios = Servicio.query.all()
    print(servicios)
    return servicios

def get_articulos():
    articulos = Articulo.query.all()
    return articulos

def register_articulo(n_articulo, desc_articulo, v_articulo,q_Articulo, k_proveedor):
    articulo = Articulo(n_articulo = n_articulo, desc_articulo = desc_articulo, v_articulo = v_articulo,q_Articulo = q_Articulo, k_proveedor=k_proveedor)
    try:
        db.session.add(articulo)
        db.session.commit()
        return articulo
    except Exception as e:
        print ("No se registró el proveedor "+ str(e))
        return None    

def register_servicio(n_servicio, desc_servicio):
    servicio = Servicio(n_servicio = n_servicio, desc_servicio = desc_servicio, e_servicio = 'ACTIVO')
    try:
        db.session.add(servicio)
        db.session.commit()
        return servicio
    except Exception as e:
        print ("No se registró el servicio "+ str(e))
        return None     
    
def register_cliente(id_cliente, n_cliente, tel_cliente, email_cliente):
    cliente  = Cliente(id_cliente=id_cliente, n_cliente=n_cliente,tel_cliente=tel_cliente,email_cliente=email_cliente)
    try:
        db.session.add(cliente)
        db.session.commit()
        return cliente
    except Exception as e:
        print("No se pudo registar el cliente "+str(e))
        return None

def consultar_cliente (id_cliente):
    try:
        cliente = Cliente.query.filter_by(id_cliente=id_cliente).first()
        print("CLIENTE!!!!")
        return cliente
    except Exception as e:
        print("Error consultando cliente ")
        return cliente
    
def obtener_ventas_diarias():

    ventas_diarias = db.session.query(
        db.func.date(Venta.f_venta).label('fecha'),
        db.func.sum(Venta.v_total_venta).label('total_venta')
    ).group_by(db.func.date(Venta.f_venta)).all()

    return ventas_diarias

def new_venta(k_cliente,k_usuario, items):
    print("FUNCION CREAR VENTA>>>>>> cliente es ", k_cliente, "yo soy  ", k_usuario, items)
    
    try:
        lstItems = []
        lstServicios = []
        total = 0
        for item in items:
            i = Item(k_articulo =  item["k_articulo"], k_servicio =  item["k_servicio"], q_item =  item["q_item"], vu_item = item["vu_item"] )
            lstItems.append(i)
            existing_servicio = next((s for s in lstServicios if s.k_servicio == item["k_servicio"]), None)
            if existing_servicio is None:
                s = Servicio_Venta(k_servicio=item["k_servicio"], v_agregado=1000)
                lstServicios.append(s)
            total += float(item["vu_item"]) * int(item["q_item"])


        venta = Venta(k_cliente = k_cliente, k_usuario = k_usuario, v_total_venta=total)
        
        db.session.add(venta)
        db.session.commit()
        id_venta_generada = venta.id
        print("ID VENTA ES ", str(id_venta_generada))
        for item in lstItems:
            item.k_venta = venta.id
            db.session.add(item)
        
        for servicio in lstServicios:
            servicio.k_venta = venta.id
            db.session.add(servicio)
        


        db.session.commit()
        print("Venta creada!!!")

        return venta
    except Exception as e:
        print("Error registrando la venta " + str(e))
        return None

def get_servicio_by_id(k_servicio):
    servicio_qs = Servicio.query.filter_by(id = k_servicio).first()
    servicio_schema = ServicioSchema()
    s = servicio_schema.dump(servicio_qs)
    return s

def get_articulo_by_id(k_producto):
    articulo_qs = Articulo.query.filter_by(id = k_producto).first()
    articulo_schema = ArticuloSchema()
    a = articulo_schema.dump(articulo_qs)
    return a

def  crear_item_producto(k_producto):
    item_qs = Articulo.query.filter_by(id = k_producto).first()
    item_schema = ItemSchema()
    i = item_schema.dump(item_qs)
    
    return i
