#Archivo principal que ejecuta flask
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app=app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
jwt = JWTManager(app)

#Cargo la variable de entorno (.env)
load_dotenv()

#Vistas que va a ejecutar flask
from app.views import view