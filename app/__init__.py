from .config import  ProductionConfig, DevelopmentConfigMYSQL, DevelopmentConfigSQLITE
from flask import Flask, session

from .database import db, ma
from .touchcenter.views import home, venta, admin, proveedor, articulo,servicio, cliente, dash_route

from flask_jwt_extended import JWTManager
from flask import Flask, render_template
from flask_assets import Environment, Bundle
from  .dash.dash_app import init_dashboard



#ACTIVE_ENDPOINTS = [('/',home), ('/dashboard', dashboard), ('/releases', releases), ('/artists', artists), ('/purchase', purchase), ("/products", products) ]
ACTIVE_ENDPOINTS = [('/',home), ('/articulo',articulo), ('/venta', venta), ('/admin', admin), ('/proveedor', proveedor), ("/servicio", servicio), ('/cliente', cliente) , ("/dash", dash_route) ]


def create_app(config=DevelopmentConfigSQLITE):
    app = Flask(__name__)
    app.debug = True 
    app.config.from_object(config)
    #app.config.from_envvar('CONFIG_SETTINGS')

    db.init_app(app)
    ma.init_app(app)
    assets = Environment(app)
    # Registra los activos para el Dash renderer y estilo
    dash_renderer_bundle = Bundle('dash-renderer.js', 'dash.css', output='gen/dash_renderer.js')
    assets.register('dash_renderer', dash_renderer_bundle)
    jwt = JWTManager(app)
    app.config['SECRET_KEY'] = 'holaMundo'
    
    

    with app.app_context():
        database.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    app = init_dashboard(app)
    return app



if __name__ == "__main__":
    app_flask = create_app()

    print("DEBUG" + str(app_flask.debug))
    app_flask.run()