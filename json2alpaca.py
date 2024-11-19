import json

def convert_to_alpaca_json(parsed_data):
    alpaca_data = []

    # Iterate through content to process Chương, Mục, and Điều
    for chuong in parsed_data["content"]:
        chuong_name = chuong["chuong"]
        for muc in chuong["muc"]:
            for dieu in muc["dieu"]:
                # Build the instruction for each Điều
                sub_clause_texts = []  # List to hold all sub-clauses under a Điều
                
                # Collect the sub-clauses (Điểm a), Điểm b), Điểm c), Điểm d)) under each numbered clause
                for clause in dieu["content"]:
                    # Add the numbered clause to the instruction
                    clause_text = f"{clause['number']}. {clause['text']}"
                    
                    # If there are lettered sub-clauses, append them as well
                    for sub_clause in clause["sub_clauses"]:
                        sub_clause_texts.append(f"[Điểm {sub_clause['letter']}] [Khoản {clause['number']}] [{dieu['id']}] [{chuong_name}] {sub_clause['text']}")

                    # Append the numbered clause and its sub-clauses to the final output
                    if sub_clause_texts:
                        clause_text += " " + " ".join(sub_clause_texts)

                    # Add the instruction for this Điều
                    alpaca_item = {
                        "instruction": f"[Khoản {clause['number']}] [{dieu['id']}] [{chuong_name}] có các điều khoản nào?", 
                        "input": "",
                        "output": clause_text
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