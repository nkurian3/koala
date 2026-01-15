# Naomi Kurian, Isabel Zheng, Veronika Duvanova, Ashley Li
# Koala
# SoftDev
# P02 – Makers Makin' It, Act I
# 2026-01-08

import sqlite3
import random
from flask import Flask, url_for, render_template
from flask import session, request, redirect
import os
#import requests
import time
import urllib.request
import urllib.error
import json


# Flask
app = Flask(__name__)
app.secret_key = "afsdfhbksadbfh"
url_err = "url error"
# SQLite
DB_FILE = "data.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

db = get_db()
c = db.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    enclosures INTEGER,
    animals INTEGER,
    money INTEGER,
    food INTEGER)
    """
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS animals (
    animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    species TEXT,
    health INTEGER,
    name TEXT,
    path TEXT,
    released INTEGER,
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
        
        money = fetch('users', 'user_id = ?', 'money', (session["user_id"],))[0][0]
        feed = fetch('users', 'user_id = ?', 'food', (session["user_id"],))[0][0]

        t = ""
        t = tableString(0)

        if request.method == "POST":
            if request.form.get("action") == "buyingF":
                
                if money >= 10:
                    db = sqlite3.connect(DB_FILE)
                    c = db.cursor()

                    c.execute('''UPDATE users 
                    SET money = money - 10
                    WHERE user_id = ?
                    ''', (session["user_id"],))

                    c.execute('''UPDATE users 
                    SET food = food + 1
                    WHERE user_id = ?
                    ''', (session["user_id"],))

                    db.commit()
                    db.close()
                    money = fetch('users', 'user_id = ?', 'money', (session["user_id"],))[0][0]
                    feed = fetch('users', 'user_id = ?', 'food', (session["user_id"],))[0][0]
                else:
                    return render_template("home.html", table = t, money = money, food = feed, error = "Not enough money!")


            if request.form.get("action") == "buyingE":
                
                if money >= 50:
                    db = sqlite3.connect(DB_FILE)
                    c = db.cursor()

                    c.execute('''UPDATE users 
                    SET money = money - 50
                    WHERE user_id = ?
                    ''', (session["user_id"],))

                    c.execute('''UPDATE users 
                    SET enclosures = enclosures + 1
                    WHERE user_id = ?
                    ''', (session["user_id"],))

                    db.commit()
                    db.close()
                    money = fetch('users', 'user_id = ?', 'money', (session["user_id"],))[0][0]
                    enclosures = fetch('users', 'user_id = ?', 'enclosures', (session["user_id"],))[0][0]
                    t = tableString(0)

                else:
                    return render_template("home.html", table = t, money = money, food = feed, error = "Not enough money!")

        return render_template("home.html", table = t, money = money, food = feed, error = "")


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
                "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    u_id,
                    request.form["username"],
                    request.form["password"],
                    3,
                    0,
                    0,
                    0
                )
            )
            db.commit()
            db.close()
            session["user_id"] = fetch("users", "username = ?", "user_id", (request.form["username"],))[0][0]
            return redirect("/")
    return render_template("register.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    ans = fetch('animals', 'user_id = ? AND released == ?', 'name', (session["user_id"], 1,))
    names = []
    for i in range(len(ans)):
        names += ans[i]
        print(names)

    ans2 = fetch('animals', 'user_id = ? AND released == ?', 'path', (session["user_id"], 1,))
    paths = []
    for i in range(len(ans2)):
        paths += ans2[i]


    tableString = ""
    for i in range(len(ans)):
        if (i%3==0):
            tableString +="<tr class= 'flex justify-between p-5'>"
        
        tableString+= f"""
        <td class = "p-4">
            <h2>{names[i]}</h2>
            <img src={paths[i]} alt="animal" class=" top-0 z-0 animalsh">
        </td>"""
        if (i%3==2):
            tableString +="</tr>"
    if not tableString.strip().endswith("</tr>"):
        tableString+="</tr>"
    
    user = fetch('users', 'user_id = ?', 'username', (session["user_id"],))[0][0]
    return render_template("profile.html", table = tableString, user = user)

@app.route("/wild", methods=["GET", "POST"])
def wild():
    anim = []
    names = ["Isabel", "Henry", "Sally", "Chris", "Patricia", "Julia"]
    healths = []
    species = []

    basepath = "static/animal_animations"
    r = random.randint(1, 6)


    for i in range(r):
        image = random.choice(os.listdir(basepath))
        if image == ".DS_Store":
            image = "bear_idle.gif"
        path = os.path.join(basepath, image)
        anim += [path]
        
        ima = image[:-4]
        arr = ima.split("_")
        print(arr)
        healths += [arr[1]]
        species += [arr[0]]


    currAns = fetch('users', 'user_id = ?', 'animals', (session["user_id"],))[0][0]
    currEns = fetch('users', 'user_id = ?', 'enclosures', (session["user_id"],))[0][0]
    space = currEns > currAns


    if request.method == "POST":
        if request.form.get("action") == "rescue":
            r = random.randint(2,7)


            basepath = "/static/animal_animations"
            image = request.form.get("species") + "_" + request.form.get("health") + ".gif"
            path = os.path.join(basepath, image)
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute('''UPDATE users 
            SET animals = animals + 1
            WHERE user_id = ?
            ''', (session["user_id"],))
            print(fetch('users', 'user_id = ?', 'animals', (session["user_id"],))[0][0])
            c.execute('''
            INSERT INTO animals (user_id, species, health, name, path, released)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (session["user_id"], request.form.get("species"), r, request.form.get("name"), path, 0,))

            db.commit()
            db.close()


            ray = str(r)

            a = fetch('animals', True, 'COUNT(*)')[0][0]
            
        return redirect(f"/enclosure/{a}")
           
           # a = fetch('animals', True, 'COUNT(*)')[0][0]
           # ev
           # return redirect(f"/enclosure/{a}")


    return render_template("wild.html", anim = anim, names = names[:r], healths = healths, species = species, space = space)




@app.route('/enclosure/<a_rowid>', methods=["GET", "POST"]) 
def enclosure(a_rowid):
    print("a_rowid = " + a_rowid)
    
   
    if request.method == "POST":
        if request.form.get("action") == "feeding":
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute('''UPDATE animals 
            SET health = health + 1
            WHERE animal_id = ?
            ''', (int(request.form.get("id")),))
           
            c.execute('''UPDATE users 
            SET food = food - 1
            WHERE user_id = ?
            ''', (session["user_id"],))

            db.commit()
            db.close()


        if request.form.get("action") == "releasing":
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()

            c.execute('''UPDATE users 
            SET animals = animals - 1
            WHERE user_id = ?
            ''', (session["user_id"],))

            c.execute('''UPDATE animals 
            SET released = 1
            WHERE animal_id = ?
            ''', (int(request.form.get("id")),))
            db.commit()
            db.close()
            return redirect("/")

    #info for food percentages--animal starts with random health below 100
    ev = fetch('animals', 'animal_id = ?', '*', (a_rowid,))
    rad = str(ev[0][4] * 10) + "%"
    strR = "width:" + rad
    ra = ev[0][4] * 10
    n = ev[0][5]

    #check if food is available
    currF = fetch('users', 'user_id = ?', 'food', (session["user_id"],))[0][0]
    canFeed = currF > 0

    return render_template("enclosure.html", p = ev[0][6], r = rad, strR = strR, rInt = ra, n = n, a = a_rowid, canFeed = canFeed)




def getTrivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    data = get_data(url)
    if not data or "results" not in data: 
        return {"question": "Error fetching question.", "correct": "", "answers": []}
    q = data["results"][0]
    question = q["question"]
    correct = q["correct_answer"]
    incorrect = q["incorrect_answers"]
    answers = incorrect + [correct]
    random.shuffle(answers)
    return {"question": question, "correct": correct, "answers": answers}

@app.route("/rewards", methods=["GET", "POST"])

def rewards():
    if "user_id" not in session: 
        return redirect ("/login")
    response = ""
    db = get_db() 
    money = db.execute("SELECT money FROM users WHERE user_id = ?", (session["user_id"],)).fetchone()[0]
    trivia = session.get ("trivia") 
    
    if not trivia: 
        trivia = getTrivia() 
        session ["trivia"] = trivia
        session ["correct_answer"] = trivia["correct"]

    if request.method == "POST": 
        selected = request.form.get ("answer")
        correct = session.get ("correct_answer")
        if selected == correct: 
            db.execute ("UPDATE users SET money = money + 30 WHERE user_id = ?", (session["user_id"],))
            db.commit() 
            money += 30
            response = "Correct! Here's 30 coins!"
        else: 
            response = f"Incorrect! The correct answer was: {correct}"
    #reloads another question & updates info
        trivia = getTrivia()
        session ["trivia"] = trivia
        session ["correct_answer"] = trivia["correct"]
    db.close()
    return render_template("rewards.html", question = trivia["question"], answers = trivia["answers"], response = response, money = money)


#helper fxns



def fetch(table, criteria, data, params=()):
    db = get_db()
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.close()
    return data

def get_data(url):
    try:
        response = urllib.request.urlopen(url) # This sends the HTTP GET request to Nasa API and urlopen returns a response obj.
        data = response.read().decode() # This decodes the response, which is in bytes, into string and then loads the json string into a python dictionary: data.
        return json.loads (data)
    except Exception as e:
        print ("Error fetching trivia:", e)
        return None 

def tableString(r):
    ans = fetch('animals', 'user_id = ? AND released == ?', 'name', (session["user_id"], r,))
    names = []
    for i in range(len(ans)):
        names += ans[i]
        print(names)

    ans2 = fetch('animals', 'user_id = ? AND released == ?', 'path', (session["user_id"], r,))
    paths = []
    for i in range(len(ans2)):
        paths += ans2[i]

    ans3 = fetch('animals', 'user_id = ? AND released == ?', 'animal_id', (session["user_id"], r,))
    ids = []
    for i in range(len(ans3)):
        ids += ans3[i]

    tableString = ""


    for i in range(fetch('users', 'user_id = ?', 'enclosures', (session["user_id"],))[0][0]):
        if (i%3==0):
            tableString +="<tr class= 'flex justify-between p-5'>"
        
        tableString+= f"""
        <td class = "p-4">"""
        if i < len(names):
            tableString+=f"""
            <h2>{names[i]}'s Enclosure</h2>
            <form action="/enclosure/{ids[i]}" method="get">
            <button>
            <div class="relative">
            <img src={paths[i]} alt="animal" class=" top-0 z-0 absolute animalsh">
            """

        else:
            tableString+="""
            <h2>Empty Enclosure</h2>
            """

        tableString += """
            <img src="static/backdrops/enclosure_backdrop.png" alt="enclosure" class =" top-0 z-10">
            </div>
            </button>
            </form>
        </td>"""
        if (i%3==2):
            tableString +="</tr>"
    if not tableString.strip().endswith("</tr>"):
        tableString+="</tr>"

    return tableString

# Flask
if __name__ == "__main__":
    app.debug = True
    app.run()
