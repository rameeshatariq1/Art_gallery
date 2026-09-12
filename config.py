import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret-key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'shop.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---- Email settings (order aane par tumhe notify karega) ----
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')       # tumhara gmail
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')       # gmail app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    # Jispe order notification email jaayegi (tumhara khud ka email)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # WhatsApp business number (jo site par bhi dikhega)
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '923064028722')
