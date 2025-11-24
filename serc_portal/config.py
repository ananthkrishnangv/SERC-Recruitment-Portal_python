import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///serc_portal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '20971520'))
    MAX_PHOTO_SIZE = int(os.getenv('MAX_PHOTO_SIZE', '102400'))
    MAX_SIGN_SIZE = int(os.getenv('MAX_SIGN_SIZE', '51200'))
    MAX_PDF_SIZE = int(os.getenv('MAX_PDF_SIZE', '5242880'))
    CLOSING_DATE = os.getenv('CLOSING_DATE', '2025-12-22')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'no-reply@serc.res.in')
