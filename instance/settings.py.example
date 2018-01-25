""" These settings are dummy settings and should really be set in instance/settings.py file"""
from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'insecurekeyfordev'

WTF_CSRF_ENABLED = False

# SQLAlchemy.
""" username and pass in db_uri must match from .env file (POSTGRES_USER=) (POSTGRES_PASSWORD=) """
db_uri = 'postgresql://funandprofit:devpassword@postgres:5432/funandprofit'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_FIRST_NAME = 'funandprofitadmin'
SEED_ADMIN_STUDENT_NUMBER = '31'
SEED_ADMIN_EMAIL = 'funandprofit@local.dev'
REMEMBER_COOKIE_DURATION = timedelta(days=1)

#Mail
MAIL_DEFAULT_SENDER = 'contact@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'awesomepassword'

#Cisco Spark
SPARK_BOT_TOKEN = ''
SPARK_BOT_EMAIL = ''
SPARK_BOT_ROOM_ID = ''
