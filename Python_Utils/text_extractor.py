import pdfplumber
import os

def extract_text_from_pdf(file_path):
    """Extract text from all pages of a PDF."""
    extracted_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:  # Ensure the page has content
                extracted_pages.append((page_number, text))
    return extracted_pages

# Path to your PDF file
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "../Textbooks/javanotes9.pdf")

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Save the raw text to a file for inspection
with open("raw_text.txt", "w", encoding="utf-8") as file:
    for page_number, page_text in extracted_text:
        file.write(f"--- Page {page_number} ---\n")
        file.write(page_text + "\n\n")
