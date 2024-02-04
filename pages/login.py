from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from app import *

import numpy as np
from werkzeug.security import check_password_hash
from flask_login import login_user
import plotly.express as px
from dash.exceptions import PreventUpdate

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center'
}

# Aqui é uma função porque é possivel controlar melhor o que vai aparecer na página se caso ocorrer um erro por exemplo.
def render_layout(message):
    message = 'Ocorreu um erro durante o login.' if message == 'error' else '',
    login = dbc.Card([
                html.Legend("login"),
                dbc.Input(id='user_login',placeholder='Username',type='text'),
                dbc.Input(id='pwd_login',placeholder='Password',type='password',style={'margin-top':'15px','margin-bottom':'15px'}),
                dbc.Button('Login',id='login_button'),
                html.Span(message,style={'text-align':'center'}),  
                html.Div([
                    html.Label('Ou', style={'margin-right':'5px'}),
                    dcc.Link('Registre-se',href="/register"),
                ], style={'padding':'20px','justify-content':'center','display':'flex'})



    ], style=card_style)
    return login 


@app.callback(
    Output('login-state','data'),
    Input('login_button','n_clicks'),

    [State('user_login','value'),
     State('pwd_login','value')]
)
def successfull(n_clicks,username,password):
    # Flesk Login (Precisa fazer alterações no código: importar o flesk_login current_user e ajustar o 'loginManager()')    
    if n_clicks == None:
        raise PreventUpdate
    #Users.query.get(int(user_id))
    user = Users.query.filter_by(username=username).first()
    # import pdb
    # pdb.set_trace()
    if user and password is not None:
         if check_password_hash(user.password, password):
             login_user(user)
             return 'success'
         else:
             return 'error'
    else:
        return 'error'
