import hashlib
import os
import traceback
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers import Response as BaseResponse

from eventpix.event_extracter import EventExtracter
from eventpix.image2text import Image2Text

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
def upload() -> BaseResponse:
    file = request.files["image"]
    image_path = save(file)
    image2text = Image2Text(image_path)
    image2text.detect_text()

    event_extractor = EventExtracter(image2text.output_text_path)
    events = event_extractor.events
    ics_content = event_extractor.get_ics_content()

    # ics_contentを保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ics_filename = f"generated_{timestamp}.ics"
    ics_content_path = Path(__file__).parent / "upload" / ics_filename
    ics_content_path.write_text(ics_content, encoding="utf8")

    for event in events:
        event.google_calendar_url = event.generate_google_calendar_url()

    session["ics_filename"] = ics_filename

    return redirect(url_for("result_view"))


@app.route("/result_view", methods=["GET"])
def result_view() -> str:
    ics_filename = session.get("ics_filename")
    if ics_filename is None:
        raise ValueError("ics_filename is None")
    ics_path = Path(__file__).parent / "upload" / ics_filename
    events = EventExtracter.ics2events(ics_path)
    return render_template("result.html", events=events, ics_filename=ics_filename)


@app.route("/sample_result_view", methods=["GET"])
def sample_result_view() -> str:
    sample_dir = Path(__file__).parent / "sample"
    ics_path = sample_dir / "sample.ics"
    ics_text = ics_path.read_text(encoding="utf8")
    events = EventExtracter.ics2events(ics_text)
    return render_template("result.html", events=events, is_sample=True)


@app.route("/download_generated_ics")
def download_generated_ics() -> BaseResponse:
    filename = request.args.get("filename")
    if filename is None:
        return BaseResponse("Filename is required", status=400)
    ics_path = Path(__file__).parent / "upload" / filename
    return send_file(ics_path, as_attachment=True, download_name=filename)


@app.route("/download_sample_ics")
def download_sample_ics() -> BaseResponse:
    ics_path = Path(__file__).parent / "sample" / "sample.ics"
    return send_file(ics_path, as_attachment=True, download_name="sample.ics")


@app.route("/sample_error_view")
def sample_error_view() -> BaseResponse:
    try:
        0 / 0
    except Exception as e:
        raise e
    return redirect(url_for("index"))


@app.errorhandler(Exception)
def handle_exception(e: Exception) -> BaseResponse:
    app.logger.error(traceback.format_exc())
    flash(str(e), "error")
    return redirect(url_for("index"))


def main() -> None:
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
