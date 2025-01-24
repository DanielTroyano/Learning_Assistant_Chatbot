import re
import json
import os

def parse_text_to_structure(raw_text_path):
    """Parse raw text into a structured JSON format."""
    structured_data = []
    current_chapter = None
    current_section = None
    current_chapter_number = None  # To track the active chapter number

    # Regular expressions to detect chapters and sections
    chapter_pattern = re.compile(r"^CHAPTER (\d+)\b", re.IGNORECASE)
    section_pattern = re.compile(r"^(\d+\.\d+)\s+(.+)")
    page_marker_pattern = re.compile(r"^--- Page \d+ ---")

    with open(raw_text_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # Skip empty lines or page markers
        if not line or page_marker_pattern.match(line):
            continue

        # Check for chapter headers
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            chapter_number = chapter_match.group(1)
            # Only create a new chapter if the chapter number changes
            if chapter_number != current_chapter_number:
                # Save the previous chapter
                if current_chapter:
                    structured_data.append(current_chapter)
                # Start a new chapter
                current_chapter = {
                    "chapter_number": chapter_number,
                    "chapter_title": None,  # Title will be added if found
                    "sections": [],
                    "content": []
                }
                current_chapter_number = chapter_number
                current_section = None  # Reset the current section
            continue  # Skip processing further since it's just a chapter header

        # Check for sections
        section_match = section_pattern.match(line)
        if section_match and current_chapter:
            # Start a new section within the current chapter
            current_section = {
                "section_number": section_match.group(1),
                "section_title": section_match.group(2),
                "content": []
            }
            current_chapter["sections"].append(current_section)
            continue

        # Add content to the current section or chapter
        if current_section:
            current_section["content"].append(line)
        elif current_chapter:
            current_chapter["content"].append(line)

    # Add the last chapter
    if current_chapter:
        structured_data.append(current_chapter)

    return structured_data

# Path to your raw text file
script_dir = os.path.dirname(os.path.abspath(__file__))
raw_text_path = os.path.join(script_dir, "../Processed_Text/Introduction_to_Programming_Using_Java/raw_text.txt")

# Parse the text file
structured_data = parse_text_to_structure(raw_text_path)

# Save to JSON
output_path = os.path.join(script_dir, "../Processed_Text/Introduction_to_Programming_Using_Java/structured_text.json")

with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

print(f"Structured text saved to {output_path}")
