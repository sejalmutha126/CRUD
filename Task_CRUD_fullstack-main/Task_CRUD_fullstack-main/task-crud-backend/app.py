from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    task = {
        "title": data["title"],
        "completed": False
    }
    result = mongo.db.tasks.insert_one(task)
    return jsonify({"id": str(result.inserted_id)})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = []
    for task in mongo.db.tasks.find():
        tasks.append({
            "_id": str(task["_id"]),
            "title": task["title"],
            "completed": task["completed"]
        })
    return jsonify(tasks)

@app.route("/tasks/<id>", methods=["PUT"])
def update_task(id):
    data = request.json
    mongo.db.tasks.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "title": data["title"],
            "completed": data["completed"]
        }}
    )
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    mongo.db.tasks.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)
