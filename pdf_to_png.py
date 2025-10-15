import fitz
from PIL import Image
import io
import sys

print(sys.argv)
if len(sys.argv) != 2:
    raise "Invalid format of command. Please repeat command in the format `python pdf_to_png.py <path to file>`"

filepath = sys.argv[1]
doc = fitz.open(filepath)

out_path = filepath.replace(".pdf", ".png")

for page_index in range(doc.page_count):
    page = doc.load_page(0)
    pixmap = page.get_pixmap(dpi=300)
    image_data = pixmap.tobytes()
    image = Image.open(io.BytesIO(image_data))
    image.save(out_path)