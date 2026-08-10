from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import os
import json

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["student_db"]
collection = db["students"]


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


if __name__ == "__main__":
    app.run(debug=True)