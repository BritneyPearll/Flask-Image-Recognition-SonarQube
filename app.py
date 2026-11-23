
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


def allowed_file(filename):
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_EXTENSIONS


def recognize_image(filename):
    filename = filename.lower()

    if "cat" in filename:
        return "Cat"
    elif "dog" in filename:
        return "Dog"
    elif "car" in filename:
        return "Car"
    else:
        return "Unknown"


@app.route("/")
def home():
    return "Flask Image Recognition Application"


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Invalid file type"}), 400

    prediction = recognize_image(image.filename)

    return jsonify({
        "filename": image.filename,
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)
