import pdfplumber
import os
import re

def clean_extracted_text(text):
    """Clean and normalize extracted text."""
    # Fix spacing issues (e.g., "Thisbookcanbe" -> "This book can be")
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Fix missing spaces between words
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)  # Add space between letters and digits
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)  # Add space between digits and letters
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = text.strip()  # Remove leading/trailing spaces
    return text

def extract_text_from_pdf(file_path):
    """Extract text from all pages of a PDF."""
    extracted_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text:  # Ensure the page has content
                # Clean and normalize text
                cleaned_text = clean_extracted_text(text)
                extracted_pages.append((page_number, cleaned_text))
    return extracted_pages

# Path to your PDF file
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "../Textbooks/Introduction_to_Programming_Using_Java.pdf")

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Save the raw text to a file for inspection
output_path = os.path.join(script_dir, "../Processed_Text/Introduction_to_Programming_Using_Java/raw_text.txt")
with open(output_path, "w", encoding="utf-8") as file:
    for page_number, page_text in extracted_text:
        file.write(f"--- Page {page_number} ---\n")
        file.write(page_text + "\n\n")

print(f"Raw text extracted and saved to {output_path}")
