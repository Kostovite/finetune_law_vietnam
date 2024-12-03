import os
import re
import json
import chardet

def detect_encoding(file_path):
    """Detect the encoding of the input file."""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

def parse_law_file(file_path):
    """Parse a single law file."""
    encoding = detect_encoding(file_path)
    print(f"Detected file encoding for {file_path}: {encoding}")
    
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
    footer_started = False

    for line in lines:
        line = line.strip()
        line = line.replace('\u00A0', ' ')

        if not line:
            continue

        # Capture the header until the body content starts
        if not body_started and not re.match(r"^(Điều\s+\d+|Chương\s+[IVXLCDM]+)", line):
            data["header"].append(line)
            continue

        # Start capturing body content when a "Điều" or "Chương" is detected
        if not body_started and re.match(r"^(Chương\s+[IVXLCDM]+|Điều\s+\d+)", line):
            body_started = True

        # Process body content and clauses
        if re.match(r"^Điều\s+\d+", line):
            if current_dieu:
                data["content"].append(current_dieu)  # Append the previous "Điều"
            parts = line.split(". ", 1)
            current_dieu = {
                "id": parts[0],
                "title": parts[1] if len(parts) > 1 else "Không có tiêu đề",
                "content": []
            }
            current_clause = None

        elif re.match(r"^\d+\.", line):
            # For numbered clauses
            parts = line.split(". ", 1)
            clause_number = parts[0].strip()
            clause_text = parts[1] if len(parts) > 1 else ""
            clause = {
                "number": clause_number,
                "text": clause_text,
                "sub_clauses": []
            }
            if current_dieu:
                current_dieu["content"].append(clause)
                current_clause = clause

        elif re.match(r"^[a-zđ]\)", line):
            # For sub-clauses
            parts = line.split(") ", 1)
            sub_clause = {
                "letter": parts[0],
                "text": parts[1] if len(parts) > 1 else ""
            }
            if current_clause and "sub_clauses" in current_clause:
                current_clause["sub_clauses"].append(sub_clause)

        elif current_clause:
            # Append to the current clause text
            current_clause["text"] += f" {line}"

        elif current_dieu:
            # Append to the current article text (no clause yet)
            if not current_dieu["content"]:
                current_dieu["content"].append({
                    "number": "0",
                    "text": line,
                    "sub_clauses": []
                })
            else:
                current_dieu["content"][-1]["text"] += f" {line}"

        # Footer starts after encountering specific phrases
        if not footer_started and (
            "Bộ luật này" in line or 
            "Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam" in line
        ):
            footer_started = True
        
        if footer_started:
            data["footer"].append(line)

    # Append the last "Điều" after processing all lines
    if current_dieu:
        data["content"].append(current_dieu)

    # Ensure footer starts after the last "Điều"
    while data["header"] and re.match(r"^(Chương\s+[IVXLCDM]+|Điều\s+\d+)", data["header"][-1]):
        data["header"].pop()

    return data

def convert_folder_to_json(input_folder, output_folder):
    """Process all .txt files in the input folder and save as JSON in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_name = os.path.splitext(file_name)[0] + ".json"
            output_file_path = os.path.join(output_folder, output_file_name)

            try:
                law_data = parse_law_file(input_file_path)
                with open(output_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(law_data, json_file, ensure_ascii=False, indent=4)
                print(f"Processed and saved: {output_file_path}")
            except Exception as e:
                print(f"Failed to process {input_file_path}: {e}")

# Example usage
input_folder = "Vietnam-Law-txt"
output_folder = "Vietnam-Law-tree_json"
convert_folder_to_json(input_folder, output_folder)