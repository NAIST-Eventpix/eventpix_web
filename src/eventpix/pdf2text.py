from pypdf import PdfReader


class Pdf2Text:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = self.get_text()

    def get_text(self) -> str:
        reader = PdfReader(self.pdf_path)
        number_of_pages = len(reader.pages)

        extract_text = ""

        for page_number in range(number_of_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            extract_text += text

        return extract_text


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    pdf2text = Pdf2Text(pdf_path)
    print(pdf2text.text)
