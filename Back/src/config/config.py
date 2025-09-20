import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # --- AÑADE ESTA LÍNEA ---
    # Mercado Pago
    MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')
    
    # Application
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'