import hashlib
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers import Response as BaseResponse

from eventpix.event_extracter import EventExtracter
from eventpix.image2text import Image2Text

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = "secret_key"

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)


def save(file: FileStorage) -> Path:
    content = file.read()
    hash = hashlib.md5(content).hexdigest()

    if file.filename is None:
        raise ValueError("file.filename is None")

    suffix = Path(file.filename).suffix
    upload_dir = Path(__file__).parent / "upload"
    upload_dir.mkdir(exist_ok=True)
    path = upload_dir / f"{hash}{suffix}"
    path.write_bytes(content)
    return path


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
@limiter.limit("100/day;5/hour")
def upload() -> str:
    try:
        file = request.files["image"]

        image_path = save(file)
        image2text = Image2Text(image_path)

        image2text.detect_text()
        events = EventExtracter(image2text.output_text_path).events
    except Exception as e:
        raise e

    return render_template("upload.html", events=events)


@app.route("/sample_result_view", methods=["GET"])
def sample_result_view() -> str:
    sample_dir = Path(__file__).parent / "sample"
    ics_path = sample_dir / "sample.ics"
    ics_text = ics_path.read_text(encoding="utf8")
    events = EventExtracter.ics2events(ics_text)
    return render_template("upload.html", events=events)


@app.route("/sample_error_view")
def sample_error_view() -> BaseResponse:
    try:
        0 / 1
    except Exception as e:
        raise e
    return redirect(url_for("index"))


@app.errorhandler(Exception)
def handle_exception(e: Exception) -> BaseResponse:
    flash(str(e), "error")
    return redirect(url_for("index"))


def main() -> None:
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
