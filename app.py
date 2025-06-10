import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "my-default-secret")

# Beispielnutzer
users = {"jose": ("jose", "1234")}

@app.route("/")
def home():
    return render_template("home.html", name=session.get("username", "Unknown"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username][1] == password:
            session["username"] = username
            return redirect(url_for("intranet"))
        else:
            return render_template("login.html", error="Falsche Zugangsdaten")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username not in users:
            users[username] = (username, password)
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error="Benutzer existiert bereits")
    return render_template("register.html")

@app.route("/intranet")
def intranet():
    if "username" in session:
        return render_template("intranet.html", user=session["username"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
