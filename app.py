from flask import Flask, request

app = Flask(__name__)

# Simpan log ke file logs.txt
def save_log(ip, user_agent):
    with open("logs.txt", "a") as f:
        f.write(f"IP: {ip}, User-Agent: {user_agent}\n")

@app.route("/log", methods=["POST"])
def log_ip():
    ip = request.remote_addr  # Dapatkan IP pengunjung
    data = request.json
    user_agent = data.get("userAgent", "Unknown")  # Ambil User-Agent

    save_log(ip, user_agent)  # Simpan ke file logs.txt
    return {"status": "logged"}, 200

@app.route("/logs", methods=["GET"])
def get_logs():
    with open("logs.txt", "r") as f:
        logs = f.readlines()
    return "<br>".join(logs) or "No logs yet."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
