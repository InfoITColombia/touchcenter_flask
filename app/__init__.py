from .config import  ProductionConfig, DevelopmentConfigMYSQL, DevelopmentConfigSQLITE
from flask import Flask, session

from .database import db, ma
from .touchcenter.views import home, venta, admin, proveedor, articulo,servicio, cliente

from flask_jwt_extended import JWTManager
from flask import Flask, render_template
from dash import Dash, html
import dash_core_components as dcc
from .dash import dash_app


#ACTIVE_ENDPOINTS = [('/',home), ('/dashboard', dashboard), ('/releases', releases), ('/artists', artists), ('/purchase', purchase), ("/products", products) ]
ACTIVE_ENDPOINTS = [('/',home), ('/articulo',articulo), ('/venta', venta), ('/admin', admin), ('/proveedor', proveedor), ("/servicio", servicio), ('/cliente', cliente)  ]


def create_app(config=DevelopmentConfigMYSQL):
    app = Flask(__name__)
    app.debug = True 
    app.config.from_object(config)
    #app.config.from_envvar('CONFIG_SETTINGS')

    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)
    app.config['SECRET_KEY'] = 'holaMundo'
    
    
    app_dash = Dash(__name__, server=app, url_base_pathname='/dash/')
    app_dash.layout =dash_app.main_app_dash.layout

    with app.app_context():
        database.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app



if __name__ == "__main__":
    app_flask = create_app()
    print("DEBUG" + str(app_flask.debug))
    app_flask.run()