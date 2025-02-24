from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Database sederhana untuk menyimpan data
def save_data(ip, user_agent):
    conn = sqlite3.connect("log.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (ip TEXT, user_agent TEXT)")
    cursor.execute("INSERT INTO logs (ip, user_agent) VALUES (?, ?)", (ip, user_agent))
    conn.commit()
    conn.close()

@app.route("/")
def track():
    ip = request.remote_addr  # Dapatkan IP target
    user_agent = request.headers.get('User-Agent')  # Dapatkan info perangkat target

    # Simpan data ke database
    save_data(ip, user_agent)

    # Redirect ke tujuan asli (misal YouTube)
    return redirect("https://www.notion.so/")

@app.route("/logs")
def view_logs():
    conn = sqlite3.connect("log.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    data = cursor.fetchall()
    conn.close()
    
    # Tampilkan hasil log
    return "<br>".join([f"IP: {row[0]}, User-Agent: {row[1]}" for row in data])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
