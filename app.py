from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB URI (Render Environment Variable se aayega)
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["event_management"]
users_collection = db["users"]
events_collection = db["events"]

# =========================
# HOME ROUTE (TEST)
# =========================
@app.route("/")
def home():
    return "Backend running successfully"

# =========================
# REGISTER API
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return jsonify({"message": "User registered successfully"})

# =========================
# LOGIN API
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({
        "email": email,
        "password": password
    })

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    })

# =========================
# ADD EVENT API
# =========================
@app.route("/add-event", methods=["POST"])
def add_event():
    data = request.json

    title = data.get("title")
    date = data.get("date")
    location = data.get("location")

    if not title or not date or not location:
        return jsonify({"message": "All fields are required"}), 400

    events_collection.insert_one({
        "title": title,
        "date": date,
        "location": location
    })

    return jsonify({"message": "Event added successfully"})

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run()
