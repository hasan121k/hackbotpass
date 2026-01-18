import pytz
from datetime import datetime
from config import Config

def get_bd_time():
    """Returns current time object in Bangladesh timezone"""
    tz = pytz.timezone(Config.TIMEZONE)
    return datetime.now(tz)

def generate_dynamic_password():
    """Generates password: monirul + HMM (12 Hour format without leading zero)"""
    now = get_bd_time()
    
    # %I হলো ১২ ঘণ্টার ফরম্যাট (যেমন 02, 12)
    # int() ব্যবহার করায় শুরুর শূন্য (0) চলে যাবে। (02 হয়ে যাবে 2)
    hour = int(now.strftime("%I"))
    minute = now.strftime("%M")
    
    return f"monirul{hour}{minute}"
