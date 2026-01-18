from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
import database as db
import threading
import bot
import time
import sys

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_db()

# --- Bot Runner (Updated) ---
def run_bot():
    # 1. Give the server a moment to start
    time.sleep(2)
    
    print("--- 🔄 ATTEMPTING TO START BOT ---", flush=True)
    
    try:
        # 2. Remove any existing webhook (Fixes the silence issue)
        bot.bot.remove_webhook()
        time.sleep(1)
        print("--- ✅ WEBHOOK REMOVED ---", flush=True)
    except Exception as e:
        print(f"--- ⚠️ WEBHOOK REMOVE ERROR: {e} ---", flush=True)

    # 3. Start Polling Loop
    while True:
        try:
            print("--- 🚀 BOT POLLING STARTED ---", flush=True)
            # interval=0 means it checks instantly
            bot.bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"--- ❌ BOT CRASHED: {e} ---", flush=True)
            time.sleep(5)
            print("--- 🔄 RESTARTING BOT ---", flush=True)

# Start bot in a separate thread
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# --- Routes ---

def is_logged_in():
    return session.get('logged_in')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check against Config
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in(): return redirect(url_for('login'))
    
    vouchers = db.get_all_vouchers()
    stats = db.get_analytics()
    current_channel = db.get_channel_id()
    
    return render_template('dashboard.html', vouchers=vouchers, stats=stats, channel=current_channel)

@app.route('/create_voucher', methods=['POST'])
def create_voucher():
    if not is_logged_in(): return redirect(url_for('login'))
    
    minutes = request.form.get('minutes')
    max_use = request.form.get('max_use')
    custom_code = request.form.get('custom_code')
    
    if minutes and max_use:
        code, msg = db.create_voucher(minutes, max_use, custom_code)
        flash(f'Result: {code if code else msg}')
    
    return redirect(url_for('dashboard'))

@app.route('/toggle/<code>')
def toggle_voucher(code):
    if not is_logged_in(): return redirect(url_for('login'))
    db.toggle_pause_voucher(code)
    return redirect(url_for('dashboard'))

@app.route('/delete/<code>')
def delete_voucher(code):
    if not is_logged_in(): return redirect(url_for('login'))
    db.delete_voucher(code)
    return redirect(url_for('dashboard'))

@app.route('/set_channel', methods=['POST'])
def set_channel():
    if not is_logged_in(): return redirect(url_for('login'))
    chat_id = request.form.get('chat_id')
    db.set_channel_id(chat_id)
    flash('Channel Updated')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT)
