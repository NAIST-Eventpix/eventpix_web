# Please setting
# https://book.st-hakky.com/data-science/data-science-gcp-vision-api-setting/

# this library need to read heif file
import io

from dotenv import load_dotenv
from PIL import Image
from pillow_heif import register_heif_opener  # type: ignore[import-untyped]

register_heif_opener()
load_dotenv()


def _get_image_binary(imagepath: str) -> bytes:
    img_bytes = io.BytesIO()
    img = Image.open(imagepath)
    img = img.convert("RGB")
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()


def detect_text(imagepath: str) -> tuple[str, str]:
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    # with open(imagepath, "rb") as image_file:
    #     content = image_file.read()

    content = _get_image_binary(imagepath)
    image = vision.Image(content=content)

    response = client.document_text_detection(
        image=image, image_context={"language_hints": ["ja"]}
    )

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    text = str(response.full_text_annotation.text)
    json = str(response)

    return text, json


if __name__ == "__main__":
    text, json = detect_text("../../sample/sample_image.jpg")
    with open("../../sample/sample_image.txt", "w", encoding="utf8") as f:
        f.write(text)
    with open("../../sample/sample_image.json", "w", encoding="utf8") as f:
        f.write(json)
