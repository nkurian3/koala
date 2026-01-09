# Naomi Kurian, Isabel Zheng, Veronika Duvanova, Ashley Li
# Koala
# SoftDev
# P02 – Makers Makin' It, Act I
# 2026-01-08

import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect
import os
import requests
import time

# Flask
app = Flask(__name__)
app.secret_key = "bdzfgetdzhezt"

# SQLite
DB_FILE = "data.db"

db = get_db()
c = db.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    )
    """
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS animals (
    animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    enclosure_number INTEGER,
    last_fed INTEGER,
    species TEXT,
    habitat INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id))
    """
)

db.commit()
db.close()


# HTML PAGES
# LANDING PAGE
@app.route("/", methods=["GET", "POST"])
def homepage():
    if not "user_id" in session:
        return redirect("/login")
    else:
        return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if not request.form["username"] in usernames:
            return render_template("login.html", error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        elif (request.form["password"] != fetch("users", "username = ?", "password", (request.form["username"],))[0][0]):
            return render_template("login.html", error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        else:
            session["user_id"] = fetch("users", "username = ?", "user_id", (request.form["username"],))[0][0]
    if "user_id" in session:
        return redirect("/")
    session.clear()
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if request.form["username"] in usernames:
            return render_template("register.html", error="Username already taken, please try again! <br><br>")
        elif request.form["password"] != request.form["confirm"]:
            return render_template("register.html", error="Passwords don't match! <br><br>")
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute("SELECT COUNT(*) FROM users")
            u_id = c.fetchall()[0][0]
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?)",
                (
                    u_id,
                    request.form["username"],
                    request.form["password"],
                )
            )
            db.commit()
            db.close()
            session["user_id"] = fetch("users", "username = ?", "user_id", (request.form["username"],))[0][0]
            return redirect("/")
    return render_template("register.html")
