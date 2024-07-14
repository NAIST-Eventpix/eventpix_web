from spire.pdf import (  # type: ignore[import-untyped]
    PdfDocument,
    PdfTextExtractOptions,
    PdfTextExtractor,
)


class Pdf2Text:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = self.get_text()

    def get_text(self) -> str:
        pdf = PdfDocument()
        pdf.LoadFromFile(self.pdf_path)

        extracted_text = ""

        extract_options = PdfTextExtractOptions()
        extract_options.IsSimpleExtraction = True

        for i in range(pdf.Pages.Count):
            page = pdf.Pages.get_Item(i)
            text_extractor = PdfTextExtractor(page)
            text = text_extractor.ExtractText(extract_options)
            extracted_text += text

        pdf.Close()

        return extracted_text


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    pdf2text = Pdf2Text(pdf_path)
    print(pdf2text.text)
