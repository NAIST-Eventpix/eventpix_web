import hashlib
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage

from eventpix import event_extracter
from eventpix.image2text import Image2Text

load_dotenv(override=True)
app = Flask(__name__)


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


@app.route("/test_result_view", methods=["GET"])
def test_result_view() -> str:
    sample_dir = Path(__file__).parent / "sample"
    ics_path = sample_dir / "sample.ics"
    ics_text = ics_path.read_text(encoding="utf8")
    cal = event_extracter.get_calender(ics_text)
    return render_template("upload.html", events=cal.walk("VEVENT"))


@app.route("/upload", methods=["POST"])
def upload() -> str:
    file = request.files["image"]
    image_path = save(file)
    image2text = Image2Text(image_path)
    image2text.detect_text()
    cal = event_extracter.read(image2text.output_text_path)
    return render_template("upload.html", events=cal.walk("VEVENT"))


def main() -> None:
    app.run(debug=True, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()
