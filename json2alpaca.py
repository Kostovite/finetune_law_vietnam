import json

def convert_to_alpaca_json(parsed_data):
    alpaca_data = []

    # Iterate through content to process Điều
    for chuong in parsed_data["content"]:
        for muc in chuong["muc"]:
            for dieu in muc["dieu"]:
                # Collect the sub-clauses (điểm a, điểm b, etc.)
                for clause in dieu["content"]:
                    sub_clause_texts = []

                    for sub_clause in clause["sub_clauses"]:
                        sub_clause_texts.append(
                            f"[điểm {sub_clause['letter']}] [khoản {clause['number']}] [{dieu['id']}] {sub_clause['text']}"
                        )

                    # Combine everything into one output string
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
    alpaca_json = convert_to_alpaca_json(parsed_data)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(alpaca_json, json_file, ensure_ascii=False, indent=4)
    print(f"Alpaca JSON saved to {output_path}")

# Example usage:
input_json_file = "luat_viet_nam.json"  # Path to the parsed law JSON
output_alpaca_file = "alpaca_format.json"  # Output path for Alpaca JSON

# Read the previously parsed law data from JSON
with open(input_json_file, "r", encoding="utf-8") as json_file:
    law_data = json.load(json_file)

# Save the Alpaca JSON version
save_alpaca_json(law_data, output_alpaca_file)