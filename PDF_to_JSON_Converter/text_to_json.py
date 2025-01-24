import re
import json
import os

def parse_text_to_structure(raw_text_path):
    """Parse raw text into a structured JSON format."""
    structured_data = []
    current_chapter = None
    current_section = None

    # Patterns for chapters and sections
    chapter_pattern_large = re.compile(r"^Chapter (\d+)\s*[:|-]?\s*(.+)?$", re.IGNORECASE)
    chapter_pattern_small = re.compile(r"^\d+\s+CHAPTER (\d+)\.\s+(.+)", re.IGNORECASE)
    section_pattern = re.compile(r"^(\d+\.\d+)\s+(.+)")
    page_marker_pattern = re.compile(r"^--- Page \d+ ---")

    with open(raw_text_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # Skip empty lines or page markers
        if not line or page_marker_pattern.match(line):
            continue

        # Check for large chapter headers
        chapter_match_large = chapter_pattern_large.match(line)
        if chapter_match_large:
            chapter_number = chapter_match_large.group(1)
            chapter_title = chapter_match_large.group(2) or f"Chapter {chapter_number}"
            chapter_description = ""
            # Save the current chapter if it exists
            if current_chapter:
                structured_data.append(current_chapter)
            # Start a new chapter
            current_chapter = {
                "chapter_number": chapter_number,
                "chapter_title": chapter_title,
                "chapter_description": "",
                "sections": [],
                "content": []
            }
            current_section = None  # Reset the current section
            continue

        # Check for small chapter headers (ignore or handle them)
        chapter_match_small = chapter_pattern_small.match(line)
        if chapter_match_small and current_chapter:
            # Optionally handle small chapter headers, e.g., append content
            current_chapter["content"].append(line)
            continue

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
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

print(f"Structured text saved to {output_path}")
