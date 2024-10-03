from flask import Flask
from flask_talisman import Talisman
import os
# from config import Config
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='assets')
# app.config.from_object(Config)
# db = SQLAlchemy(app)

if os.environ.get('FLASK_ENV') == 'production':
    csp = {
        'default-src': ["'self'"],
        'style-src': ["'self'", 'https://cdn.jsdelivr.net'],
        'script-src': ["'self'", 'https://cdn.jsdelivr.net', 'https://www.googletagmanager.com'],
        'img-src': ["'self'", 'data:'],  # Allow 'self' and 'data:' for images
    }

    # Apply the custom CSP using Flask-Talisman
    Talisman(app, content_security_policy=csp)

from app import routes
