import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_TIMEOUT = 10
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.environ.get("EMAIL_USER")
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')
    CLOUDINARY_CLOUD_NAME=os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.environ.get("CLOUDINARY_API_SECRET")
    
    SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300
    }
