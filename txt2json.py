import chardet
import re
import json

def detect_encoding(file_path):
    """Detect the encoding of the input file."""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']
        
def parse_law_file(file_path):
    # Automatically detect the file encoding
    encoding = detect_encoding(file_path)
    print(f"Detected file encoding: {encoding}")
    
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()
    
    data = {
        "header": [],
        "content": [],
        "footer": []
    }

    current_dieu = None
    current_clause = None
    body_started = False
    last_body_line_index = None

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Detect header (before the first Điều)
        if not body_started and not re.match(r"^Điều\s+\d+", line):
            data["header"].append(line)
            continue

        # Detect Điều
        if re.match(r"^Điều\s+\d+", line):
            body_started = True
            if current_dieu:
                data["content"].append(current_dieu)
            parts = line.split(". ", 1)
            current_dieu = {
                "id": parts[0],
                "title": parts[1] if len(parts) > 1 else "",
                "content": []
            }
            current_clause = None
            last_body_line_index = i  # Update last body line index

        # Detect numbered clauses (e.g., "1.", "2.")
        elif re.match(r"^\d+\.", line):
            parts = line.split(". ", 1)
            clause = {
                "number": parts[0],
                "text": parts[1] if len(parts) > 1 else "",
                "sub_clauses": []
            }
            if current_dieu:
                current_dieu["content"].append(clause)
                current_clause = clause

        # Detect lettered sub-clauses (e.g., "a)", "b)")
        elif re.match(r"^[a-z]\)", line):
            parts = line.split(") ", 1)
            sub_clause = {
                "letter": parts[0],
                "text": parts[1] if len(parts) > 1 else ""
            }
            if current_clause and "sub_clauses" in current_clause:
                current_clause["sub_clauses"].append(sub_clause)

        # Handle continuation lines for clauses
        elif current_clause and "text" in current_clause:
            current_clause["text"] += f" {line}"

    # Add the last Điều to the content
    if current_dieu:
        data["content"].append(current_dieu)

    # Capture footer content (after the last body line)
    if last_body_line_index is not None:
        data["footer"] = [
            line.strip() for line in lines[last_body_line_index + 1:] if line.strip()
        ]

    return data

# Convert the parsed data to JSON
def convert_to_json(file_path, output_path):
    law_data = parse_law_file(file_path)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(law_data, json_file, ensure_ascii=False, indent=4)
    print(f"Data successfully converted and saved to {output_path}")


# Example usage
input_file = "luat_viet_nam.txt"  # Replace with the correct file path
output_file = "luat_viet_nam.json"
convert_to_json(input_file, output_file)