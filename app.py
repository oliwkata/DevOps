from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Nauczyć się Dockera", "done": False},
    {"id": 2, "title": "Zaliczyć projekt z DevOps", "done": False},
    {"id": 3, "title": "Odpocząć po sesji", "done": False},
]


@app.get("/")
def index():
    return """
    <h1>Simple Tasks App</h1>
    <p>To jest bardzo prosta aplikacja do zaliczenia Dockera.</p>
    <ul>
      <li>Sprawdź <code>/api/health</code> – zdrowie aplikacji.</li>
      <li>Sprawdź <code>/api/tasks</code> – lista przykładowych zadań.</li>
    </ul>
    """


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
