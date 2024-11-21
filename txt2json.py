import re
import json
import chardet

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
    footer_started = False

    # Use Unicode flag for proper matching
    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Detect header (before the first Điều or Chương)
        if not body_started and not re.match(r"^(Điều\s+\d+|Chương\s+[IVXLCDM]+)", line, re.UNICODE):
            data["header"].append(line)
            continue

        # Detect the start of the body (Chương or Điều)
        if not body_started and re.match(r"^(Chương\s+[IVXLCDM]+|Điều\s+\d+)", line, re.UNICODE):
            body_started = True

        # Detect footer start
        if body_started and re.match(r"^(Luật này đã được Quốc hội|CHỦ TỊCH QUỐC HỘI)", line, re.UNICODE):
            footer_started = True

        if footer_started:
            data["footer"].append(line)
            continue

        # Detect Điều
        if re.match(r"^Điều\s+\d+", line, re.UNICODE):
            if current_dieu:
                data["content"].append(current_dieu)
            parts = line.split(". ", 1)
            current_dieu = {
                "id": parts[0],
                "title": parts[1] if len(parts) > 1 else "",
                "content": []
            }
            current_clause = None
            last_body_line_index = i

        # Detect numbered clauses (e.g., "1.", "2.")
        elif re.match(r"^\d+\.", line, re.UNICODE):
            parts = line.split(". ", 1)
            clause = {
                "number": parts[0],
                "text": parts[1] if len(parts) > 1 else "",
                "sub_clauses": []
            }
            if current_dieu:
                current_dieu["content"].append(clause)
                current_clause = clause

        # Modify this part where sub-clause detection occurs
        elif re.match(r"^[a-zđ]\)", line):
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

    # Clean up the header to ensure it ends before Chương or Điều
    while data["header"] and re.match(r"^(Chương\s+[IVXLCDM]+|Điều\s+\d+)", data["header"][-1], re.UNICODE):
        data["header"].pop()

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