from flask import Flask, render_template, request, jsonify
import sqlite3
import os
app = Flask(__name__)

def db():
    return sqlite3.connect("database.db")

def init_db():
    con = db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance REAL DEFAULT 0
    )
    """)
    con.commit()
    con.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/user", methods=["POST"])
def user():
    data = request.json
    user_id = data["id"]
    username = data.get("username", "غير معروف")

    con = db()
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?,?)",
                (user_id, username))
    con.commit()

    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = cur.fetchone()[0]
    con.close()

    return jsonify({"balance": balance})

@app.route("/api/action", methods=["POST"])
def action():
    action = request.json["action"]
    return jsonify({"msg": f"✅ تم تنفيذ: {action}"})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)