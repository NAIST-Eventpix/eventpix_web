from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index() -> str:
    return "Hello from Flask!"


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
