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
        'style-src': [
            "'self'",
            'https://cdn.jsdelivr.net',
            "unsafe-inline",  # Allow inline styles
            # "'sha256-6Q5F2pMp/C1Og2TFlm4KzLyq/tDZsPkvIu9Od1sj7HQ='",  # Specific hash if applicable
            "unsafe-hashes",
            "https://www.google-analytics.com"
        ],
        'script-src': [
            "'self'", 'https://cdn.jsdelivr.net', 'https://www.googletagmanager.com',"'sha256-KZMiy1Q3T0ILCRXdaWG0niQoK89rZuJyry8S6ohvMbY='"
        ],
        'img-src': ["'self'", 'data:', "https://www.google-analytics.com"],
        'connect-src': ["'self'", "https://www.google-analytics.com"],
    }

    # Apply the custom CSP using Flask-Talisman
    Talisman(app, content_security_policy=csp)

    # Talisman(app, force_https=True)

from app import routes
