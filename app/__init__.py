from flask import Flask
from flask_talisman import Talisman
import os
# from config import Config
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='assets')
# app.config.from_object(Config)
# db = SQLAlchemy(app)

if os.environ.get('FLASK_ENV') == 'production':
    Talisman(app)

from app import routes
