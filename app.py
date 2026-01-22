from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://agarwalkritika218_db_user:yncuizyQ16cHGWTu@cluster0.g9jiia3.mongodb.net/event_management?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client["event_management"]
users_collection = db["users"]
events_collection = db["events"]

@app.route("/")
def home():
    return "Backend running successfully"

# 🔹 REGISTER API
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    user = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password")
    }

    users_collection.insert_one(user)

    return jsonify({
        "message": "User registered successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)