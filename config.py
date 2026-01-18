import os

class Config:
    # Render Environment Variables
    PORT = int(os.environ.get("PORT", 5000))
    
    # টোকেনটি অবশ্যই এই লাইনের সোজাসুজি (Indented) হতে হবে
    BOT_TOKEN = "8360585659:AAEQQIk4nG-hHxWuFW1qz_Q4Gdhqcf_UJI0"
    
    # Admin Credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "admin123")
    
    # App Config
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")
    TIMEZONE = 'Asia/Dhaka'
    DB_NAME = "data.db"
