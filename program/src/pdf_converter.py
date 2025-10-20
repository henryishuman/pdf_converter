import io
from typing import List
from os import path

import fitz
from PIL import Image

class PDFConverter:
    filepath: str
    read_data: List[bytes]
    pdf_doc: fitz.Document

    def __init__(self, filepath):
        if not path.exists(filepath):
            raise FileNotFoundError(filepath)

        self.filepath = filepath
        self.read(filepath)

    def read(self, filepath: str):
        if not filepath.endswith(".pdf"):
            raise IOError("File must be a PDF: " + filepath)

        self.read_data = []
        self.pdf_doc = fitz.open(f"{filepath}")
        for page_index in range(self.pdf_doc.page_count):
            page = self.pdf_doc.load_page(page_index)
            pixmap = page.get_pixmap(dpi=300)
            page_data = pixmap.tobytes()
            self.read_data.append(page_data)

    def save_as_pdf(self, filepath: str):
        filepath = filepath.replace(".pdf", "")
        self.pdf_doc.save(f"{filepath}.pdf")

    def save_as_image(self, filepath: str):
        if self.pdf_doc.page_count == 1:
            image = Image.open(io.BytesIO(self.read_data[0]))
            image.save(filepath)
        else:
            for page_index in range(self.pdf_doc.page_count):
                image = Image.open(io.BytesIO(self.read_data[page_index]))
                full_file_path = f"{path.splitext(filepath)[0]}_{page_index}{path.splitext(filepath)[1]}"
                image.save(full_file_path)