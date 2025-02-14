from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from utils import load_users, save_users
from datetime import datetime

auth = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin):
    def __init__(self, id, name, patient_id, gender, phone, email, password, dob):
        self.id = id
        self.name = name
        self.patient_id = patient_id
        self.gender = gender
        self.phone = phone
        self.email = email
        self.password = password
        self.dob = datetime.strptime(dob, "%Y-%m-%d") if isinstance(dob, str) else dob  # Convert string to datetime

@login_manager.user_loader
def load_user(user_id):
    users = load_users()["users"]
    for user in users:
        if user["id"] == int(user_id):
            return User(user["id"], user["name"], user["patient_id"], user["gender"], user["phone"], user["email"], user["password"], user["dob"])
    return None

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        patient_id = request.form["patient_id"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        dob = request.form["dob"]  # Expecting input as YYYY-MM-DD format

        users = load_users()
        user_id = len(users["users"]) + 1
        users["users"].append({
            "id": user_id,
            "name": name,
            "patient_id": patient_id,
            "gender": gender,
            "phone": phone,
            "email": email,
            "password": password,
            "dob": dob  # Store as a string
        })
        save_users(users)
        flash("Account created! You can log in now.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")
