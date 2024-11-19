import json
import re
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
        "footer": []  # Add a footer section
    }
    
    current_chuong = None
    current_muc = None
    current_dieu = None
    current_clause = None  # To track the current numbered clause

    # Variables to track the line index of the last body item
    last_body_item_index = None

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines
        if not line:
            continue
        
        # Detect headers (before any Chương)
        if not current_chuong and not re.match(r"^Chương\s+[IVXLCDM]+", line):
            data["header"].append(line)
            continue
        
        # Detect Chương
        if re.match(r"^Chương\s+[IVXLCDM]+", line):
            if current_chuong:
                if current_muc:
                    current_chuong["muc"].append(current_muc)
                data["content"].append(current_chuong)
            current_chuong = {
                "chuong": line,
                "muc": []
            }
            current_muc = None
            current_dieu = None
            current_clause = None  # Reset current clause when a new Chương is found
        
        # Detect Mục
        elif re.match(r"^Mục\s+\d+", line):
            if current_muc:
                current_chuong["muc"].append(current_muc)
            current_muc = {
                "muc": line,
                "dieu": []
            }
            current_dieu = None
        
        # Detect Điều (Numbered clause)
        elif re.match(r"^Điều\s+\d+", line):
            if current_dieu:
                if current_muc:
                    current_muc["dieu"].append(current_dieu)
                elif current_chuong:
                    current_chuong["muc"].append({"dieu": [current_dieu]})
            parts = line.split(". ", 1)
            current_dieu = {
                "id": parts[0],
                "title": parts[1] if len(parts) > 1 else "",
                "content": []  # This holds the numbered and lettered sub-clauses
            }
            current_clause = current_dieu  # Track the current clause
            
        # Detect numbered clauses (e.g., "1.", "2.") under a Điều
        elif re.match(r"^\d+\.", line):
            parts = line.split(". ", 1)
            clause = {
                "number": parts[0],
                "text": parts[1] if len(parts) > 1 else "",
                "sub_clauses": []  # Initialize an empty list for sub-clauses (letters)
            }
            if current_dieu:
                current_dieu["content"].append(clause)
                current_clause = clause  # The clause becomes the current clause for sub-clauses
        
        # Detect lettered clauses (e.g., "a)", "b)") under the previous numbered clause
        elif re.match(r"^[a-z]\)", line):
            parts = line.split(") ", 1)
            sub_clause = {
                "letter": parts[0],
                "text": parts[1] if len(parts) > 1 else ""
            }
            if current_clause and "sub_clauses" in current_clause:
                current_clause["sub_clauses"].append(sub_clause)
        
        # Handle continuation lines (for multi-line clauses)
        elif current_clause and "text" in current_clause:
            current_clause["text"] += f" {line}"

        # Update the last body item index when we process the last item
        if current_clause and re.match(r"^\d+\.", line):  # Ensure it's a numbered body item
            last_body_item_index = i

    # Finalize last structures
    if current_dieu:
        if current_muc:
            current_muc["dieu"].append(current_dieu)
        elif current_chuong:
            current_chuong["muc"].append({"dieu": [current_dieu]})
    if current_muc:
        current_chuong["muc"].append(current_muc)
    if current_chuong:
        data["content"].append(current_chuong)

    # If we have a valid index for the last body item, capture everything after it as footer
    if last_body_item_index is not None:
        # Add all lines after the last body item to the footer, excluding empty ones
        data["footer"] = [line.strip() for line in lines[last_body_item_index + 1:] if line.strip()]

    return data

# Convert the parsed data to JSON
def convert_to_json(file_path, output_path):
    law_data = parse_law_file(file_path)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(law_data, json_file, ensure_ascii=False, indent=4)
    print(f"Data successfully converted and saved to {output_path}")

# Example usage
input_file = "luat_viet_nam.txt"  # Update the path if needed
output_file = "luat_viet_nam.json"
convert_to_json(input_file, output_file)