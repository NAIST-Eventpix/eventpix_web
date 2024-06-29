# Please setting
# https://book.st-hakky.com/data-science/data-science-gcp-vision-api-setting/

# this library need to read heif file
import io
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image
from pillow_heif import register_heif_opener  # type: ignore[import-untyped]

register_heif_opener()
load_dotenv()


class Image2Text:
    def __init__(self, imagepath: Path) -> None:
        self._imagepath = imagepath
        self._hash = imagepath.stem

        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        self._output_text_path = output_dir / f"{self._hash}.txt"
        self._output_json_path = output_dir / f"{self._hash}.json"

    @property
    def output_text_path(self) -> Path:
        return self._output_text_path

    @property
    def output_json_path(self) -> Path:
        return self._output_json_path

    def _get_image_binary(self) -> bytes:
        img_bytes = io.BytesIO()
        img = Image.open(self._imagepath)
        img = img.convert("RGB")
        img.save(img_bytes, format="JPEG")
        return img_bytes.getvalue()

    def _save(self, res_text: str, res_json: str) -> None:
        self._output_text_path.write_text(res_text, encoding="utf8")
        self._output_json_path.write_text(res_json, encoding="utf8")

    def detect_text(self) -> None:
        """Detects text in the file."""
        from google.cloud import vision

        client = vision.ImageAnnotatorClient()
        content = self._get_image_binary()
        image = vision.Image(content=content)

        response = client.document_text_detection(
            image=image, image_context={"language_hints": ["ja"]}
        )

        if response.error.message:
            raise Exception(
                f"{response.error.message}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors"
            )

        res_text = str(response.full_text_annotation.text)
        res_json = str(response)

        self._save(res_text, res_json)
