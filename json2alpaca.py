import json

def convert_to_alpaca_json(parsed_data):
    alpaca_data = []

    # Extract relevant parts from header
    header = parsed_data["header"]
    # Header elements are split into different parts (first item can be special)
    law_title = header[6]  # Assuming "LUẬT DƯỢC" is at index 6

    # Iterate through the content to create Alpaca JSON
    for chuong in parsed_data["content"]:
        chuong_name = chuong["chuong"]
        for muc in chuong["muc"]:
            for dieu in muc["dieu"]:
                # Create a structure for each "Điều"
                alpaca_item = {
                    "instruction": f"[{dieu['id']}] [{chuong_name}] có các điều khoản nào?",
                    "input": "",
                    "output": "\n".join([f"{clause['number']}. {clause['text']}" for clause in dieu["content"]])
                }
                alpaca_data.append(alpaca_item)

                # Handle sub-clauses under each numbered clause (if any)
                for clause in dieu["content"]:
                    if clause["sub_clauses"]:
                        for sub_clause in clause["sub_clauses"]:
                            alpaca_sub_item = {
                                "instruction": f"[{dieu['id']}] [{chuong_name}] có khoản con nào?",
                                "input": "",
                                "output": f"{sub_clause['letter']}) {sub_clause['text']}"
                            }
                            alpaca_data.append(alpaca_sub_item)

    return alpaca_data

def save_alpaca_json(parsed_data, output_path):
    alpaca_json = convert_to_alpaca_json(parsed_data)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(alpaca_json, json_file, ensure_ascii=False, indent=4)
    print(f"Alpaca JSON saved to {output_path}")

# Example usage:
# Assuming you have parsed the law file into `law_data`
input_json_file = "luat_viet_nam.json"
output_alpaca_file = "alpaca_format.json"

# Read the previously parsed law data from JSON
with open(input_json_file, "r", encoding="utf-8") as json_file:
    law_data = json.load(json_file)

# Save the Alpaca JSON version
save_alpaca_json(law_data, output_alpaca_file)