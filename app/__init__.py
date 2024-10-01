from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='assets')
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes
