from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
