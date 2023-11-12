from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response
from .forms import LoginUsuarioForm, RegistroUsuarioForm, newClienteForm, newArticuloForm
from .models import get_user_by_usuario, register_user
from flask_jwt_extended import create_access_token, verify_jwt_in_request
import datetime
from datetime import timedelta
from functools import wraps
import jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity

home = Blueprint('home', __name__)
producto = Blueprint('producto', __name__ , url_prefix = '/producto')
venta = Blueprint('venta',       __name__ , url_prefix = '/venta')
admin = Blueprint('admin',       __name__ , url_prefix = '/admin')



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
            flash("error", ("Su sesión expiró " ))
            return redirect(url_for('home.logout'))

        return f(*args, **kwargs)

    return decorated



@venta.before_request
@admin.before_request
@producto.before_request
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
            flash('info', "Bienvenido")
            access_token = create_access_token(identity=user["n_usuario"], expires_delta=datetime.timedelta(seconds=10))
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
   

@producto.route("/", methods=["GET", "POST"])
def productos():
    return "Productos"

@venta.route("/", methods=["GET", "POST"])
def ventas():
    if request.method == "GET":
        return render_template('ventas.html')

@venta.route("/nuevo", methods=["GET", "POST"])
def nuevaventa():

    form_new_cliente = newClienteForm()
    form_new_articulo = newArticuloForm()
    if request.method == "GET":
        return render_template('nuevaVenta.html', form_new_cliente = form_new_cliente, form_new_producto = form_new_articulo)

@admin.route("/", methods=["GET", "POST"])
def dash():
    form_new_cliente = newClienteForm()
    form_new_articulo = newArticuloForm()
    if request.method == "GET":
        return render_template('admin.html', form_new_cliente = form_new_cliente, form_new_producto = form_new_articulo)