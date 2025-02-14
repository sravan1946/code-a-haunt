import uuid
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from utils import load_users, save_users
from datetime import datetime

auth = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin):
    def __init__(self, pid, name, email, password, phone_no, gender, DOB):
        self.pid = pid
        self.name = name
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.gender = gender
        self.DOB = DOB

    def get_id(self):
        return str(self.pid)

    def __dict__(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone_no": self.phone_no,
            "gender": self.gender,
            "DOB": self.DOB,
        }
@login_manager.user_loader
def load_user(user_id):
    users = load_users()["users"]
    for user in users:
        if user["pid"] == int(user_id):
            return User(**user)
    return None

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pid: int = int(str(uuid.uuid4().int)[:14])
        name: str = request.form["name"]
        email: str = request.form["email"]
        password: str = request.form["password"]
        phone_no: int = request.form["phone"]
        gender: str = request.form["gender"]
        DOB: datetime.date = request.form["dob"]
        user = User(
            pid=pid,
            name=name,
            email=email,
            password=password,
            phone_no=phone_no,
            gender=gender,
            DOB=DOB,
        )
        users = load_users()
        if user.email in [user["email"] for user in users["users"]]:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))
        if user.phone_no in [user["phone_no"] for user in users["users"]]:
            flash("Phone number already exists.", "danger")
            return redirect(url_for("auth.register"))
        users["users"].append(user.__dict__())
        save_users(users)
        flash("Account created! You can log in now.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        for user in users["users"]:
            if user["email"] == email and user["password"] == password:
                user_obj = User(**user)
                login_user(user_obj)
                flash("Logged in successfully!", "success")
                return redirect(url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    flash("Logged out successfully!", "success")
    logout_user()
    return redirect(url_for("index"))
