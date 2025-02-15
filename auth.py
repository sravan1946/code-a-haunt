import uuid
from flask import Blueprint, request, redirect, session, url_for, render_template, flash
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
        DOB: str = request.form["dob"]  # Store DOB as a string

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

        users["users"].append(user.__dict__)
        save_users(users)

        # Auto-login after registration
        session["logged_in"] = True
        session["patient_id"] = pid

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.profile"))

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
                session["logged_in"] = True
                session["patient_id"] = user["pid"]
                flash("Logged in successfully!", "success")
                return redirect(url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("patient_id", None)
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))


@auth.route("/profile")
def profile():
    if "logged_in" not in session:
        flash("You must be logged in to access your profile.", "error")
        return redirect(url_for("auth.login"))
    
    return redirect(url_for("auth.profile_pid", pid=session["patient_id"]))

@auth.route("/profile/<pid>")
def profile_pid(pid):
    users = load_users()
    for user in users["users"]:
        if user["pid"] == int(pid):
            break
    else:
        user = None
    if not user:
        flash("Profile not found!", "error")
        return redirect(url_for("auth.login"))

    return render_template("profile.html", user=user)
