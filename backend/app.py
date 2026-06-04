from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "SoulSync Backend Running"

DB_NAME = "moods.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    entry TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(moods)")
    columns = [row[1] for row in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE moods ADD COLUMN user_id INTEGER")

    conn.commit()
    conn.close()


init_db()



@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data["username"].strip()
    password = data["password"].strip()

    if not username or not password:
        return jsonify({"message": "Username and password required"})

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return jsonify({"message": "Signup successful"})
    except:
        return jsonify({"message": "Username already exists"})
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"].strip()
    password = data["password"].strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "username": user[1]
        })
    else:
        return jsonify({"message": "Invalid username or password"})


@app.route("/mood", methods=["POST"])
def mood():
    data = request.get_json()

    mood_value = data.get("mood")
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"response": "Please login first"}), 401

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO moods (user_id, mood) VALUES (?, ?)",
        (user_id, mood_value)
    )

    conn.commit()
    conn.close()

    if mood_value == "sad":
        return jsonify({"response": "You seem sad 💙"})
    elif mood_value == "happy":
        return jsonify({"response": "You seem happy 🌟"})
    elif mood_value == "lonely":
        return jsonify({"response": "You seem lonely 🤍"})
    elif mood_value == "confused":
        return jsonify({"response": "You seem confused 😕"})
    else:
        return jsonify({"response": "Mood unclear 🤔"})


@app.route("/history", methods=["GET"])
def history():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify([])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, mood, created_at FROM moods WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    history_list = []
    for row in rows:
        history_list.append({
            "id": row[0],
            "mood": row[1],
            "created_at": row[2]
        })

    return jsonify(history_list)

@app.route("/journal", methods=["POST"])
def journal():
    data = request.get_json()

    entry = data.get("entry")
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "Please login first"}), 401

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO journals (user_id, entry) VALUES (?, ?)",
        (user_id, entry)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Journal saved successfully"})


@app.route("/journals", methods=["GET"])
def journals():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify([])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, entry, created_at FROM journals WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    journal_list = []
    for row in rows:
        journal_list.append({
            "id": row[0],
            "entry": row[1],
            "created_at": row[2]
        })

    return jsonify(journal_list)

@app.route("/stats", methods=["GET"])
def stats():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify([])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT mood, COUNT(*) FROM moods WHERE user_id = ? GROUP BY mood",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    stats_list = []
    for row in rows:
        stats_list.append({
            "mood": row[0],
            "count": row[1]
        })

    return jsonify(stats_list)

init_db()

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )