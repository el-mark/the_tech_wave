from flask import Flask
from flask_talisman import Talisman
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from flask_googlestorage import GoogleStorage, Bucket


app = Flask(__name__, static_folder='assets')
# app.config.from_object(Config)
# db = SQLAlchemy(app)


if os.environ.get('FLASK_ENV') == 'production':
    csp = {
        'default-src': ["'self'"],
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        # 'style-src': [
        #     # "'self'",
        #     'https://cdn.jsdelivr.net',
        #     "unsafe-inline",  # Allow inline styles
        #     # "'sha256-6Q5F2pMp/C1Og2TFlm4KzLyq/tDZsPkvIu9Od1sj7HQ='",  # Specific hash if applicable
        #     "unsafe-hashes",
        #     "https://www.google-analytics.com"
        # ],
        'script-src': [
            "'self'", 'https://cdn.jsdelivr.net', 'https://www.googletagmanager.com',
            "'unsafe-inline'"
        ],
        'img-src': ["'self'", 'data:', "https://www.google-analytics.com"],
        'connect-src': ["'self'", "https://www.google-analytics.com"],
    }

    # Apply the custom CSP using Flask-Talisman
    Talisman(app, content_security_policy=csp)

    # Talisman(app, force_https=True)

database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('DATABASE_URL')

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create a LoginManager instance
login_manager = LoginManager()
login_manager.init_app(app)

# Configure the LoginManager (optional)
# login_manager.login_view = 'login'

# Google Storage
files = Bucket("files")
storage = GoogleStorage(files)
app.config.update(
    GOOGLE_STORAGE_LOCAL_DEST=app.instance_path,
    GOOGLE_STORAGE_SIGNATURE={"expiration": timedelta(minutes=5)},
    GOOGLE_STORAGE_FILES_BUCKET="articles_images"
)
storage.init_app(app)

from app.models import User
# Define a user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes

