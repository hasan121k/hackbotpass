import os

class Config:
    # Render Environment Variables
    PORT = int(os.environ.get("PORT", 5000))
    # আপনার বটের লম্বা টোকেনটি ডাবল কোটেশন " " এর ভেতর বসান
BOT_TOKEN = "8360585659:AAEQQIK4nG-hHxWuFW1qz_Q4Gdhqcf_UJI0"
    
    # Admin Credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "admin123")
    
    # App Config
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")
    TIMEZONE = 'Asia/Dhaka'
    DB_NAME = "data.db"
