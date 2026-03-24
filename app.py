from flask import Flask, render_template, request, redirect, url_for, session,flash
from pymongo import MongoClient
import csv
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = "eventify_secret_key"
# MongoDB
MONGO_URI = "mongodb+srv://agarwalkritika218_db_user:Mongo12345@cluster0.g9jiia3.mongodb.net/event_management?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
client.admin.command("ping")
print("MongoDB connected successfully")

db = client["event_management"]
users = db["users"]
bookings = db["booking"]

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return render_template(
            "register.html",
            message="User registered successfully"
        )

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({
            "email": email,
            "password": password
        })

        if user:
            session["user_email"] = user["email"]
            session["role"] = user.get("role", "user")

            if user.get("role") == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", message="Invalid email or password")

    return render_template("login.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    all_bookings = bookings.find()
    return render_template("admin_dashboard.html", bookings=all_bookings)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route("/wedding")
def wedding():
    return render_template("wedding.html")


@app.route("/parties")
def parties():
    return render_template("parties.html")


@app.route("/concerts")
def concerts():
    return render_template("concerts.html")


@app.route("/cultural")
def cultural():
    return render_template("cultural.html")


@app.route("/catering")
def catering():
    return render_template("catering.html")


@app.route("/budget")
def budget():
    return render_template("budget.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        try:
            fullName = request.form.get("fullName")
            email = request.form.get("email")
            phone = request.form.get("phone")
            eventType = request.form.get("eventType")
            eventDate = request.form.get("eventDate")
            guests = request.form.get("guests")
            venue = request.form.get("venue")
            catering = request.form.get("catering")
            requirements = request.form.get("requirements")
            amount = request.form.get("amount")
            payment = request.form.get("payment","pending")

            # Fixed advance amount
            if eventType == "Wedding":
                amount = 200000
            elif eventType == "Birthday":
                amount = 2000
            elif eventType == "Concert":
                amount = 100000
            elif eventType == "Cultural Event":
                amount = 50000
            else:
                amount = 0

            result = bookings.insert_one({
                "fullName": fullName,
                "email": email,
                "phone": phone,
                "eventType": eventType,
                "eventDate": eventDate,
                "guests": guests,
                "venue": venue,
                "catering": catering,
                "requirements": requirements,
                "amount": amount,
                "payment":payment
            
            })

            flash("Booking Successfully Done!", "success")
            return redirect(url_for("booking"))

        except Exception as e:
            print("BOOKING ERROR:", e)
            flash("Server error", "error")
            return redirect(url_for("booking"))

    return render_template("booking.html")

if __name__ == "__main__":
    app.run(debug=True, port=10000)