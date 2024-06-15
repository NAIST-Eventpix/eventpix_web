from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index() -> str:
    return "Hello from Flask!"


@app.route("/upload", methods=["POST"])
def upload() -> str:
    file = request.files["image"]
    file.save(f"uploads/{file.filename}")
    return "Upload successful!"


def main() -> None:
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
