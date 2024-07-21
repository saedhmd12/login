from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "phpmyadmin"
app.config["MYSQL_PASSWORD"] = "Root1234!@#$"
app.config["MYSQL_DB"] = "Beirutevents"

mysql = MySQL(app)


@app.route("/login")
def form():
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        account = cursor.fetchone()
        if account:
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]

            return "Logged in successfully!"
        else:
            msg = "Incorrect username/password!"
    return render_template("login.html", msg=msg)


@app.route("/pythonlogin/register", methods=["GET", "POST"])
def register():
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["register_username"]
        password = request.form["register_password"]
        email = request.form["register_gmail"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not email:
            msg = "Please fill out the form!"
        else:
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            cursor.execute(
                "INSERT INTO users VALUES (%s, %s, %s)",
                (
                    username,
                    email,
                    password,
                ),
            )
            mysql.connection.commit()
            msg = "You have successfully registered!"
    elif request.method == "POST":
        msg = "Please fill out the form!"
    return render_template("register.html", msg=msg)


app.run(host="localhost", port=5000)
