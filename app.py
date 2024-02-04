# pip install SQLAlchemy
# pip install Flask-SQLAlchemy
# pip install flask-login
# pip install flask==2.2.5

import dash 
import dash_bootstrap_components as dbc
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import configparser
import os
import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select

# Conecta ou cria a conexão com o banco de dados
conn = sqlite3.connect('data.sqlite')
# Mantem a conexão ativa ao banco de dados
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()

#Cria a tabela de usuários
# Obs. Essa classe herdará tudo o que estiver na db.Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15),unique=True, nullable=False)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))

    def is_active(self):
        """True, as all users are active."""
        return True
    def get_id(self):
        """Return the id usuer to satisfy Flask-Login's requirements."""
        return (self.id)
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
    
    

User_tbl = Table('users', Users.metadata)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
server = app.server
app.config.suppress_callback_exceptions = True

# Modificações necessárias para o funcionamento do flask-login
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False

)

db.init_app(server)

class User(UserMixin,Users):
    pass

