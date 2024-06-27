import hashlib

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

load_dotenv(override=True)
app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Hello from Flask!"


@app.route("/upload", methods=["POST"])
def upload() -> str:
    file = request.files["image"]
    path = f"uploads/{file.filename}"
    file.save(path)
    with open(path, "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()
    return hash


def main() -> None:
    app.run(host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()
