from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response
from .forms import LoginUsuarioForm, RegistroUsuarioForm
from .models import get_user_by_usuario, register_user

home = Blueprint('home', __name__)
producto = Blueprint('producto', __name__ , url_prefix = '/producto')
venta = Blueprint('venta',       __name__ , url_prefix = '/venta')

@home.route("/")
def index():
    return render_template("home.html") 

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
        print(user)
        if not user:
            print("no existe el usuario")
            flash("No existe el usuario", 'info')
            return redirect(url_for('home.login'))
        elif user['pwd_usuario'] == pwd:
            flash("Bienvenido", 'info')
            session["user"] = user
            return redirect(url_for('home.index'))
        else:
            flash("Contraseña incorrecta", 'warning')
            return redirect(url_for('home.login'))
        

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
            flash("El usuario ya existe", 'info')
            return redirect(url_for('home.register'))
        else:
            user = register_user(usuario,pwd, "admin" )
            if user:
                flash("Se registro el usuario "+ user, 'success')
                return redirect(url_for('home.login'))
            else:
                flash( "No se registró el usuario ", 'error')
                return redirect(url_for('home.register'))
   

@producto.route("/", methods=["GET", "POST"])
def productos():
    return "Productos"

@venta.route("/", methods=["GET", "POST"])
def ventas():
    return "ventas"
