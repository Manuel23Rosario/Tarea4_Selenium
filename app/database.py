import sqlite3
from flask import g
from werkzeug.security import generate_password_hash

DATABASE = "database.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()

    # Tabla correcta (usuarios)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # Tabla correcta (propiedades)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            direccion TEXT,
            precio REAL NOT NULL
        );
    """)

    db.commit()

    # Crear admin si no existe
    cur.execute("SELECT * FROM users WHERE email = ?", ("admin@example.com",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            ("admin@example.com", generate_password_hash("password123")),
        )
        db.commit()

    db.close()