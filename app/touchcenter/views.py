from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response
from .forms import *
from .models import *
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from ..config import Config as conf


from functools import wraps
import jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..dash.dash_app import main_app_dash


home = Blueprint('home', __name__)
articulo = Blueprint('articulo', __name__ , url_prefix = '/articulo')
venta = Blueprint('venta',       __name__ , url_prefix = '/venta')
admin = Blueprint('admin',       __name__ , url_prefix = '/admin')
proveedor = Blueprint('proveedor', __name__ , url_prefix = '/proveedor')
cliente = Blueprint('cliente', __name__ , url_prefix = '/cliente')
servicio = Blueprint('servicio', __name__ , url_prefix = '/servicio')
dash_route = Blueprint('dash_route', __name__ , url_prefix = '/dash')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            #token = session.get("user")[0]["access_token"]
            token = session.get("user")["access_token"]
            #print("TOKEN " +  token)
            if not token:
                flash("error", "Error de sesión! "+str(e))

                return redirect(url_for('home.logout'))



            data = jwt.decode(token, "holaMundo", algorithms=["HS256"])
            # Realiza cualquier otra validación que necesites aquí
        except jwt.ExpiredSignatureError as e:
            print("ERROR GENERANDO EL TOKEN ! "+ str(e))
            flash("error", "Su sesión expiró!")
            session.pop("user", None)  # Elimina la sesión del usuario
            return redirect(url_for('home.logout'))
        except Exception as e:
            print("ERROR DE SESION! "+ str(e))
            #flash("error", ("Su sesión expiró " ))
            return redirect(url_for('home.logout'))

        return f(*args, **kwargs)

    return decorated



@venta.before_request
@admin.before_request
@articulo.before_request
@token_required
def validate_before_request():
    pass

@home.route("/")
@token_required
def index():
    return redirect(url_for('venta.ventas'))


@home.route("/login", methods=["GET", 'POST'])
def login():
    form_login = LoginUsuarioForm()

    if request.method == 'GET':
        resp = make_response(render_template('login.html', form=form_login))
        resp.set_cookie('same-site-cookie', 'foo', samesite='Lax')
        resp.set_cookie('cross-site-cookie', 'bar', samesite='Lax', secure=True)
        return resp

    if request.method == 'POST':
        usuario = form_login.usuario.data
        pwd = form_login.pwd_usuario.data

        user = get_user_by_usuario(usuario)

        if not user:
            print("no existe el usuario")
            flash( 'info',"No existe el usuario")
            return redirect(url_for('home.login'))
        elif user['pwd_usuario'] == pwd:
            #flash('info', "Bienvenido")
            access_token = create_access_token(identity=user["n_usuario"], expires_delta= conf.TOKEN_EXPIRES)
            session["user"] = {"n_usuario":user["n_usuario"],  "access_token":access_token} 
            print(session["user"])
            return redirect(url_for('home.index'))
        else:
            flash('warning', "Contraseña incorrecta")
            return redirect(url_for('home.login'))

@home.route("/logout",  methods=["GET", 'POST'])
def logout():
    g.user=None
    session.pop("user", None)
    print("Se cerró sesión")
    return redirect(url_for('home.login',user=g.user))
        

@home.route("/register", methods=["GET", 'POST'])
def register():
    form_register = RegistroUsuarioForm()

    if request.method == 'GET':
        #resp = make_response()
        #resp.set_cookie('same-site-cookie', 'foo', samesite='Lax')
        #resp.set_cookie('cross-site-cookie', 'bar', samesite='Lax', secure=True)
        return render_template('register.html', form=form_register)

    if request.method == 'POST':
        usuario = form_register.usuario.data
        pwd = form_register.pwd_usuario.data

        user = get_user_by_usuario(usuario)
        if user:
            flash('info', "El usuario ya existe")
            return redirect(url_for('home.register'))
        else:
            user = register_user(usuario,pwd, "admin" )
            if user:
                flash( 'success', "Se registro el usuario "+ user)
                return redirect(url_for('home.login'))
            else:
                flash( 'error', "No se registró el usuario ")
                return redirect(url_for('home.register'))
   

@articulo.route("/", methods=["GET", "POST"])
def articulos():
    return "articulos"

@venta.route("/", methods=["GET", "POST"])
def ventas():
    if request.method == "GET":
        return render_template('ventas.html')

@venta.route("/nuevo", methods=["GET", "POST"])
def nuevaventa():

    form_new_cliente = newClienteForm()
    form_new_articulo = newArticuloForm()
    form_new_proveedor = newProveedorForm()
    form_consultar_cliente = newClienteForm()
    form_new_venta  =newVentaForm()
    if request.method == "GET":
        return render_template('nuevaVenta.html', form_new_cliente = form_new_cliente, form_new_articulo = form_new_articulo, form_new_proveedor = form_new_proveedor, form_new_venta = form_new_venta, form_consultar_cliente=form_consultar_cliente)


@venta.route("/registroventa/<k_cliente>/<k_usuario>", methods=["GET", "POST"])
def registroventa(k_cliente, k_usuario):
        print("REGISTRANDO VENTA")
        form_new_cliente = newClienteForm()
        form_new_articulo = newArticuloForm()
        form_new_proveedor = newProveedorForm()
        form_consultar_cliente = newClienteForm()
        form_new_venta  =newVentaForm()
    
        print("registrando venta")
        k_cliente = k_cliente
        k_usuario = k_usuario
        k_servicio = form_new_venta.k_servicio.data
        k_item = form_new_venta.k_producto.data
        venta = new_venta(k_cliente,k_usuario,k_servicio,k_item)
        if venta:
            flash("sucess", "Venta registrada!")
            return redirect(request.referrer)
        else:
            flash("error","No se registro la venta ")
            return redirect(request.referrer)

@admin.route("/", methods=["GET", "POST"])
def dash():
    form_new_cliente = newClienteForm()
    form_new_articulo = newArticuloForm()
    form_new_proveedor = newProveedorForm()
    form_new_servicio = newServicioForm()
    if request.method == "GET":
        return render_template('admin.html', form_new_cliente = form_new_cliente, form_new_articulo= form_new_articulo, form_new_proveedor = form_new_proveedor, form_new_servicio = form_new_servicio)


@proveedor.route("/nuevo", methods=["POST"])
def nuevoProveedor():
    form_new_proveedor = newProveedorForm()
    if form_new_proveedor.validate_on_submit():
        nombre = form_new_proveedor.n_proveedor.data
        dir = form_new_proveedor.dir_proveedor.data
        tel = form_new_proveedor.tel_proveedor.data
        prov = register_proveedor(nombre, dir, tel)
        if prov:
                flash( "success", "Proveedor registrado exitosamente")
                return redirect(request.referrer)
        else:
                flash( "error", "Error al registrar proveedor")
                return redirect(request.referrer)

    # Manejo adicional para solicitudes GET o si la validación del formulario falla
    return render_template('tu_template.html', form_new_proveedor=form_new_proveedor)

@proveedor.route("/JSONProveedores", methods=["GET"])
def JSONProveedores():
    proveedores = get_proveedores() 
    # Puedes personalizar el formato JSON según tus necesidades
    proveedores_json = [{"label": str(proveedor.id) +" - "+ proveedor.n_proveedor, "value": str(proveedor.id) +" - "+ proveedor.n_proveedor} for proveedor in proveedores]
    print (proveedores_json)
    return jsonify(proveedores_json)

@servicio.route("/JSONServicios", methods=["GET"])
def JSONServicios():
    servicios = get_servicios() 
    # Puedes personalizar el formato JSON según tus necesidades
    servicios_json = [{"label": str(servicio.id) +" - "+ servicio.n_servicio, "value": str(servicio.id) +" - "+ servicio.n_servicio} for servicio in servicios]
    print (servicios_json)
    return jsonify(servicios_json)

@articulo.route("/JSONArticulos", methods=["GET"])
def JSONArticulos():
    articulos = get_articulos() 
    # Puedes personalizar el formato JSON según tus necesidades
    articulos_json = [{"label": str(articulo.id) +" - "+ articulo.n_articulo, "value": str(articulo.id) +" - "+ articulo.n_articulo} for articulo in articulos]
    print (articulos_json)
    return jsonify(articulos_json)
    

@articulo.route("/nuevo", methods=["POST"])
def nuevoArticulo():
    form_new_articulo = newArticuloForm()
    if form_new_articulo.validate_on_submit():
        n_articulo = form_new_articulo.n_articulo.data
        desc_articulo = form_new_articulo.desc_articulo.data
        v_articulo = form_new_articulo.v_articulo.data
        q_Articulo = form_new_articulo.q_articulo.data
        #k_proveedor = form_new_articulo.k_proveedor.data
        n_proveedor = form_new_articulo.n_proveedor.data
        print("el proveedor elegido es "+str(n_proveedor))
        articulo = register_articulo(n_articulo, desc_articulo, v_articulo,q_Articulo, n_proveedor.split(" - ",1)[0])
        if articulo:
                flash( "success", "Articulo registrado exitosamente")
                return redirect(request.referrer)
        else:
                flash( "error", "Error al registrar articulo")
                return redirect(request.referrer)

@servicio.route("/nuevo", methods=["POST"])
def nuevoServicio():
    form_new_servicio=newServicioForm()
    if form_new_servicio.validate_on_submit():
        n_servicio = form_new_servicio.n_servicio.data
        desc_servicio = form_new_servicio.desc_servicio.data
        servicio = register_servicio(n_servicio,desc_servicio)
        if servicio:
            flash("success", "Servicio registrado exitosamente")
            return redirect(request.referrer)
        else:
            flash( "error", "Error al registrar servicio")
            return redirect(request.referrer)

@cliente.route("/nuevo", methods=["POST"])
def nuevoCliente():
    form_new_cliente = newClienteForm()
    if form_new_cliente.validate_on_submit():
       id_cliente = form_new_cliente.id_cliente.data
       n_cliente  =form_new_cliente.n_cliente.data
       tel_cliente = form_new_cliente.tel_cliente.data
       email_cliente = form_new_cliente.email_cliente.data
       cliente = register_cliente(id_cliente,n_cliente,tel_cliente,email_cliente)
       if cliente:
            flash('success', 'Cliente '+str(cliente.id)+" registrado exitosamente")
            return redirect(request.referrer)
       else:
            flash("error", "Error al registrar cliente!")
            return redirect(request.referrer, cliente=cliente)
@cliente.route("/consultar", methods=["POST"])
def consultarCliente():
    form_consultar_cliente = newClienteForm()
    print("ESTOY AQUI")
    if request.method == 'POST':
        id_cliente = form_consultar_cliente.id_cliente.data
        cliente = consultar_cliente(id_cliente)
        if cliente:
            flash("success", "Cliente "+str(cliente.n_cliente)+" encontrado")
            session["cliente"] = {"id_Cliente": cliente.id_cliente, "n_cliente":cliente.n_cliente, "tel_cliente":cliente.tel_cliente, "email_cliente":cliente.email_cliente} 
            return redirect(request.referrer)
        else:
            flash("error", "Cliente no encontrado")
            session["cliente"] = None
            return redirect(request.referrer)
    else:
        flash("success", "No se pudo validar el formulario")
        return redirect(request.referrer)


@dash_route.route("/", methods=["GET"])
def load_dash():
    #dash_url = url_for('main_app_dash') 

    #return render_template('dash_app.html', dash_url=dash_url)
    return render_template('dash_app.html',         title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask.")

@dash_route.route("/dashboard", methods=["GET"])
def dashboard():
    return main_app_dash.layout