from flask import Flask, request, redirect, render_template_string
import sqlite3
import logging
from datetime import datetime
import threading

app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Database setup dengan threading
lock = threading.Lock()
def init_db():
    with lock:
        conn = sqlite3.connect("log.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                user_agent TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

# Fungsi menyimpan data ke database
def save_data(ip, user_agent):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with lock:
        conn = sqlite3.connect("log.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (ip, user_agent, timestamp) VALUES (?, ?, ?)", (ip, user_agent, timestamp))
        conn.commit()
        conn.close()
    logging.info(f"[LOG] IP: {ip}, User-Agent: {user_agent}, Time: {timestamp}")

@app.route("/")
def track():
    ip = request.remote_addr  # Ambil IP target
    user_agent = request.headers.get('User-Agent')  # Ambil informasi perangkat
    
    # Simpan ke database
    save_data(ip, user_agent)
    
    # Redirect ke tujuan (misal YouTube)
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@app.route("/logs")
def view_logs():
    with lock:
        conn = sqlite3.connect("log.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY id DESC")
        data = cursor.fetchall()
        conn.close()
    
    # Template HTML untuk menampilkan log
    html_template = """
    <html>
    <head>
        <title>Log IP Tracker</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            table { width: 80%; margin: auto; border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Logged IP Addresses</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>IP Address</th>
                <th>User-Agent</th>
                <th>Timestamp</th>
            </tr>
            {% for row in logs %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    
    return render_template_string(html_template, logs=data)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
