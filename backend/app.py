from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "moods.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
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

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return "SoulSync Backend Running"


@app.route("/mood", methods=["POST"])
def mood():
    data = request.get_json()
    mood_value = data["mood"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO moods (mood) VALUES (?)",
        (mood_value,)
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, mood, created_at FROM moods ORDER BY id DESC"
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


@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()

        return jsonify({
            "message": "Signup successful"
        })

    except:
        return jsonify({
            "message": "Username already exists"
        })

    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Login successful"
        })
    else:
        return jsonify({
            "message": "Invalid username or password"
        })


@app.route("/stats", methods=["GET"])
def stats():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT mood, COUNT(*) FROM moods GROUP BY mood"
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


if __name__ == "__main__":
    app.run(debug=True)