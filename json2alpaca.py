import json

def convert_to_alpaca_json(parsed_data):
    """
    Converts flattened law data into Alpaca JSON format.
    Args:
        parsed_data (dict): The parsed law JSON structure.
    Returns:
        list: A list of dictionaries in Alpaca format.
    """
    alpaca_data = []

    # Iterate through the content (Điều-level focus)
    for dieu in parsed_data["content"]:
        for clause in dieu["content"]:
            sub_clause_texts = []

            # Process sub-clauses (điểm a, điểm b, etc.)
            for sub_clause in clause.get("sub_clauses", []):
                sub_clause_texts.append(
                    f"[điểm {sub_clause['letter']}] [khoản {clause['number']}] [{dieu['id']}] {sub_clause['text']}"
                )

            # Combine the clause text and its sub-clauses
            clause_output = f"{clause['text']} {' '.join(sub_clause_texts)}"

            # Add the instruction and output for this clause
            alpaca_item = {
                "instruction": f"[khoản {clause['number']}] [{dieu['id']}] có các điều khoản nào?",
                "input": "",
                "output": clause_output.strip()
            }
            alpaca_data.append(alpaca_item)

    return alpaca_data

def save_alpaca_json(parsed_data, output_path):
    """
    Saves the Alpaca-formatted data to a JSON file.
    Args:
        parsed_data (dict): Parsed law data.
        output_path (str): File path to save the Alpaca JSON.
    """
    alpaca_json = convert_to_alpaca_json(parsed_data)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(alpaca_json, json_file, ensure_ascii=False, indent=4)
    print(f"Alpaca JSON saved to {output_path}")

# Example usage:
input_json_file = "./Vietnam-Law-tree_json/Bộ luật-45-2019-QH14.json"  # Path to the parsed law JSON
output_alpaca_file = "alpaca_format.json"  # Output path for Alpaca JSON

# Read the parsed law data from JSON
with open(input_json_file, "r", encoding="utf-8") as json_file:
    law_data = json.load(json_file)

# Save the Alpaca JSON version
save_alpaca_json(law_data, output_alpaca_file)