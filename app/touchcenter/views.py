from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response


home = Blueprint('home', __name__)


@home.route("/")
def index():
    return render_template("home.html") 

@home.route("/login", methods=["GET", 'POST'])
def login():
    form_login = LoginUsuarioForm()

    if request.method == 'POST':
        email = form_login.email_usuario.data
        pwd = form_login.pwd_usuario.data

        user = get_user_by_email(email)
        print(user)
        if not user:
            print("no existe el usuario")
            flash("No existe el usuario")
            return redirect(url_for('home.index'))
        elif user['pwd_usuario'] == pwd:
            flash("Bienvenido")
            session["user"] = user
            return redirect(url_for('home.index', user=g.user, purchase_cart = g.purchase))

    resp = make_response(render_template('login.html', form=form_login))
    resp.set_cookie('same-site-cookie', 'foo', samesite='Lax')
    resp.set_cookie('cross-site-cookie', 'bar', samesite='Lax', secure=True)
    return resp