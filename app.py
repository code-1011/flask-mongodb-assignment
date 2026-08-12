from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import os
import json

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["student_db"]

# Existing student collection
collection = db["students"]

# New To-Do collection
todo_collection = db["todos"]


@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/", methods=["GET", "POST"])
def form():
    error = None

    if request.method == "POST":
        try:
            name = request.form["name"]
            grade = request.form["grade"]

            collection.insert_one({
                "name": name,
                "grade": grade
            })

            return redirect(url_for("success"))

        except Exception as e:
            error = str(e)

    return render_template("form.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")

# To-Do item submission API
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        item_name = request.form["itemName"]
        item_description = request.form["itemDescription"]

        todo = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        todo_collection.insert_one(todo)

        return "To-Do item submitted successfully"

    except Exception as e:
        return f"Error submitting To-Do item: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
