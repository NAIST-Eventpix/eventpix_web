from pathlib import Path

from pypdf import PdfReader


class Pdf2Text:
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self._hash = pdf_path.stem

        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        self._output_text_path = output_dir / f"{self._hash}.txt"

    @property
    def output_text_path(self) -> Path:
        return self._output_text_path

    def detect_text(self) -> None:
        reader = PdfReader(self.pdf_path)
        number_of_pages = len(reader.pages)

        extract_text = ""

        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            extract_text += text

        self._save(extract_text)

    def _save(self, res_text: str) -> None:
        self._output_text_path.write_text(res_text, encoding="utf8")


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    pdf2text = Pdf2Text(pdf_path)
    print(pdf2text.text)
