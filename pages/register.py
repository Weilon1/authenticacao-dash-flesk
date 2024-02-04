from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from app import *
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash

import numpy as np
from app import *

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
    message = 'Ocorreu um erro durante o registro' if message == 'error' else ''
    register = dbc.Card([
                html.Legend("Registrar"),
                dbc.Input(id='user_register',placeholder='Username',type='text'),
                dbc.Input(id='email_register',placeholder='E-mail',type='email',style={'margin-bottom':'15px'}),
                dbc.Input(id='pwd_register',placeholder='Password',type='password',style={}),
                dbc.Button('Registre-se',id='register-button'),
                html.Span(message,style={'text-align':'center'}),
                html.Div([
                    html.Label('Ou', style={'margin-right':'5px'}),
                    dcc.Link('Faça-login',href="/login"),
                ], style={'padding':'20px','justify-content':'center','display':'flex'})



    ], style=card_style)
    return register 

@app.callback(
    Output('register-state','data'),
    Input('register-button','n_clicks'),

    [State('user_register','value'),
     State('pwd_register','value'),
     State('email_register','value')])
def register(n_clicks,username,password,email):
    if n_clicks == None:
        raise PreventUpdate

    
    if username is not None and password is not None and email is not None:
        hashed_password = generate_password_hash(password,method='sha256')
        # import pdb
        # pdb.set_trace()

        # Insere os dados na tabela que criamos 
        #ins = Users_tbl.insert().values(username=username,password=hashed_password, email=email)
        ins = User_tbl.insert().values(username=username,email=email,password=hashed_password)
        conn = engine.connect()
        conn.execute(ins)
        #conn.commit()
        conn.close()
        return ''
    else:
        return 'error'
#         # import pdb
#         # pdb.set_trace()

#         return ''
#     else:
#         return 'error'



