from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB URI from Render Environment Variable
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["event_management"]

users_collection = db["users"]
events_collection = db["events"]

@app.route("/")
def home():
    return "Backend running successfully"

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    user = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password")
    }

    users_collection.insert_one(user)

    return jsonify({"message": "User registered successfully"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
