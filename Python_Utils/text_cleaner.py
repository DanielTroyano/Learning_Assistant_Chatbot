import re

def clean_text(extracted_text):
    """Clean and structure raw text data."""
    cleaned_text = []
    for page_number, text in extracted_text:
        # Remove page numbers and extra whitespace
        text = re.sub(r"Page \d+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s{2,}", " ", text)  # Remove extra spaces
        text = text.strip()  # Remove leading/trailing whitespace
        if text:
            cleaned_text.append((page_number, text))
    return cleaned_text

# Clean the extracted text
cleaned_text = clean_text(extracted_text)

# Save cleaned text to a file for inspection
with open("cleaned_text.txt", "w", encoding="utf-8") as file:
    for page_number, text in cleaned_text:
        file.write(f"--- Page {page_number} ---\n")
        file.write(text + "\n\n")
