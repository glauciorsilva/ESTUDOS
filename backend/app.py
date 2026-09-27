"""
Backend mínimo (Flask + SQLite) para persistir o progresso do
"Prática Python para Dados" em um banco de dados de verdade,
em vez de só no localStorage do navegador.

Como rodar:
    pip install -r requirements.txt
    python app.py

O servidor sobe em http://localhost:5000
O banco fica no arquivo progresso.db, na mesma pasta deste script.
"""

import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "progresso.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            db.executescript(f.read())


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/progresso")
def listar_progresso():
    db = get_db()
    rows = db.execute("SELECT exercicio_id, concluido, codigo FROM progresso").fetchall()
    completed = [r["exercicio_id"] for r in rows if r["concluido"]]
    code = {r["exercicio_id"]: r["codigo"] for r in rows if r["codigo"] is not None}
    return jsonify({"completed": completed, "code": code})


@app.post("/api/progresso")
def salvar_progresso():
    dados = request.get_json(force=True)
    exercicio_id = dados.get("exercicio_id")
    if not exercicio_id:
        return jsonify({"erro": "exercicio_id é obrigatório"}), 400

    concluido = 1 if dados.get("concluido") else 0
    codigo = dados.get("codigo")

    db = get_db()
    db.execute(
        """
        INSERT INTO progresso (exercicio_id, concluido, codigo, atualizado_em)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(exercicio_id) DO UPDATE SET
            concluido = excluded.concluido,
            codigo = excluded.codigo,
            atualizado_em = excluded.atualizado_em
        """,
        (exercicio_id, concluido, codigo, now_iso()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.post("/api/tentativas")
def registrar_tentativa():
    dados = request.get_json(force=True)
    exercicio_id = dados.get("exercicio_id")
    if not exercicio_id:
        return jsonify({"erro": "exercicio_id é obrigatório"}), 400

    sucesso = 1 if dados.get("sucesso") else 0
    mensagem = dados.get("mensagem", "")

    db = get_db()
    db.execute(
        "INSERT INTO tentativas (exercicio_id, sucesso, mensagem, criado_em) VALUES (?, ?, ?, ?)",
        (exercicio_id, sucesso, mensagem, now_iso()),
    )
    db.commit()
    return jsonify({"ok": True})


@app.get("/api/tentativas")
def listar_tentativas():
    exercicio_id = request.args.get("exercicio_id")
    db = get_db()
    if exercicio_id:
        rows = db.execute(
            "SELECT * FROM tentativas WHERE exercicio_id = ? ORDER BY criado_em DESC",
            (exercicio_id,),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM tentativas ORDER BY criado_em DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/stats")
def estatisticas():
    db = get_db()
    rows = db.execute(
        """
        SELECT exercicio_id,
               COUNT(*) AS tentativas,
               SUM(sucesso) AS acertos
        FROM tentativas
        GROUP BY exercicio_id
        ORDER BY tentativas DESC
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
