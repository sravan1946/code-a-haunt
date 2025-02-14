from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from utils import load_users, save_users

auth = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    users = load_users()["users"]
    for user in users:
        if user["id"] == int(user_id):
            return User(user["id"], user["username"], user["password"])
    return None

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()["users"]
        for user in users:
            if user["username"] == username and user["password"] == password:
                login_user(User(user["id"], user["username"], user["password"]))
                return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        user_id = len(users["users"]) + 1
        users["users"].append({"id": user_id, "username": username, "password": password})
        save_users(users)
        flash("Account created! You can log in now.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
