TIMEZONE = 'America/Chicago'

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
import os


db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'iDiagnosis'
MAIL_PASSWORD = db_password
ADMINS = [db_user]

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12
