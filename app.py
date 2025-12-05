from flask import Flask, jsonify
import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")

app = Flask(__name__)


def init_db():
    """Tworzy bazę SQLite i przykładowe zadania, jeśli jeszcze ich nie ma."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    # jeśli tabela jest pusta, dodaj przykładowe rekordy
    cur = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Nauczyć się Dockera", 0),
                ("Zaliczyć projekt z DevOps", 0),
                ("Odpocząć po sesji", 0),
            ],
        )

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# inicjalizacja bazy przy starcie aplikacji / imporcie modułu
init_db()


@app.get("/")
def index():
    return """
    <h1>Simple Tasks App</h1>
    <p>To jest bardzo prosta aplikacja do zaliczenia DevOps.</p>
    <ul>
      <li>Sprawdź <code>/api/health</code> – zdrowie aplikacji.</li>
      <li>Sprawdź <code>/api/tasks</code> – lista zadań z bazy danych.</li>
    </ul>
    """


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/tasks")
def get_tasks():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
    conn.close()

    tasks = [
        {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        for row in rows
    ]
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
