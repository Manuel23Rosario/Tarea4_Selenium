from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
from .database import get_db, init_db
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Inicializar base de datos una sola vez
with app.app_context():
    init_db()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["email"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    db = get_db()
    cur = db.cursor()
    props = cur.execute("SELECT * FROM properties").fetchall()
    return render_template("dashboard.html", properties=props)

@app.route("/properties/new", methods=["GET", "POST"])
def property_new():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        precio = request.form.get("precio", "").strip()

        if not titulo or not precio:
            return render_template(
                "property_form.html",
                error="Titulo y precio son obligatorios",
                prop=None,
                mode="new"
            )

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO properties (titulo, direccion, precio) VALUES (?, ?, ?)",
            (titulo, direccion, float(precio))
        )
        db.commit()
        return redirect("/dashboard")

    return render_template("property_form.html", prop=None, mode="new")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/properties/edit/<int:id>", methods=["GET", "POST"])
def edit_property(id):
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    prop = db.execute("SELECT * FROM properties WHERE id = ?", (id,)).fetchone()

    if not prop:
        return redirect("/dashboard")

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        direccion = request.form["direccion"].strip()
        precio = request.form["precio"].strip()

        if not titulo or not precio:
            return render_template("property_form.html",
                                   error="Titulo y precio son obligatorios",
                                   mode="edit",
                                   prop=prop)

        try:
            precio = float(precio)
            if precio <= 0:
                raise ValueError()
        except:
            return render_template("property_form.html",
                                   error="Precio no puede ser negativo",
                                   mode="edit",
                                   prop=prop)

        db.execute(
            "UPDATE properties SET titulo=?, direccion=?, precio=? WHERE id=?",
            (titulo, direccion, precio, id)
        )
        db.commit()

        return redirect("/dashboard")

    return render_template("property_form.html", mode="edit", prop=prop)

@app.route("/properties/delete/<int:id>", methods=["POST"])
def delete_property(id):
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM properties WHERE id = ?", (id,))
    db.commit()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)