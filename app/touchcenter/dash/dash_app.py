from dash import Dash, html, dcc
from flask import Flask
from ..models import get_proveedores
import pandas as pd
from dash.dependencies import Output, Input
import plotly.express as px
from ..models import *






def init_dashboard(server, db):
    
    proveedores = db.session.query(Proveedor).all()
    articulos = db.session.query(Articulo).all()

    proveedores_data = [(proveedor.id, proveedor.n_proveedor, proveedor.dir_proveedor, proveedor.tel_proveedor) for proveedor in proveedores]
    articulos_data = [(articulo.id, articulo.n_articulo, articulo.desc_articulo, articulo.v_articulo, articulo.q_Articulo, articulo.k_proveedor) for articulo in articulos]

    proveedores_df = pd.DataFrame(proveedores_data, columns=['id_proveedor', 'n_proveedor', 'dir_proveedor', 'tel_proveedor'])
    articulos_df = pd.DataFrame(articulos_data, columns=['id_articulo', 'n_articulo', 'desc_articulo', 'v_articulo', 'q_Articulo', 'k_proveedor'])

    # Fusionar DataFrames
    merged_df = pd.merge(articulos_df, proveedores_df, left_on='k_proveedor', right_on='id_proveedor')

    # Crear el gráfico de barras
    fig_proveedores = px.bar(merged_df, x='n_proveedor', y='q_Articulo', title='Cantidad de Artículos por Proveedor')
    fig_servicios = serviciosGraph(db)
    fig_ventas = ventasGraph(db)

    print(proveedores)
    """Create a Plotly Dash dashboard."""
    main_app_dash = Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    #db.init_app(main_app_dash.server)


    # Create Dash Layout
    main_app_dash.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        dcc.Graph(
        id='example-graph',
        figure=fig_proveedores
        ),
        html.H1(children='Gráfico de Torta para Servicios'),
        dcc.Graph(
            id='pie-chart',
            figure=fig_servicios
        ),
        html.H1(children='Gráfico de Líneas Temporales para Ventas'),
        dcc.Graph(
            id='line-chart',
            figure=fig_ventas
        )
    ]
)
    return main_app_dash.server

def serviciosGraph(db):
    servicios = db.session.query(Servicio).all()
    servicios_data = {'Estado': [servicio.e_servicio for servicio in servicios]}
    df_servicios = pd.DataFrame(servicios_data)

    # Crear gráfico de torta
    fig_servicios = px.pie(df_servicios, names='Estado', title='Distribución de Servicios por Estado')
    return fig_servicios


def ventasGraph(db):
    ventas = db.session.query(Venta).all()
    ventas_data = {'Fecha de Venta': [venta.f_venta for venta in ventas],
                'Valor Total de Venta': [venta.v_total_venta for venta in ventas]}
    df_ventas = pd.DataFrame(ventas_data)

    # Crear gráfico de líneas temporales
    fig_ventas = px.line(df_ventas, x='Fecha de Venta', y='Valor Total de Venta', title='Evolución Temporal de Ventas')
    return fig_ventas