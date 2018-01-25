from flask_wtf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

csrf = CsrfProtect()
db = SQLAlchemy()
login_manager = LoginManager()
