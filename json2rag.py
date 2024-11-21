import json

def convert_to_rag_format(parsed_data):
    """
    Converts nested JSON structure into RAG-ready format with full context.
    Args:
        parsed_data (dict): The parsed law data.
    Returns:
        list: A list of dictionaries in RAG format.
    """
    rag_data = []

    # Extract global context (header and footer)
    header = " ".join(parsed_data.get("header", []))
    footer = " ".join(parsed_data.get("footer", []))

    # Build the context string
    general_context = f"{header} {footer}".strip()

    # Iterate over the content
    for dieu in parsed_data["content"]:
        article_id = dieu["id"]
        article_title = dieu.get("title", "")
        
        for clause in dieu["content"]:
            clause_number = clause.get("number", "")
            clause_text = clause.get("text", "")
            
            # Add the main clause to RAG format
            rag_data.append({
                "id": f"{article_id}.{clause_number}",
                "article": article_id,
                "clause": clause_number,
                "title": article_title,
                "text": clause_text,
                "context": general_context
            })
            
            # Add sub-clauses to RAG format
            for sub_clause in clause.get("sub_clauses", []):
                sub_clause_letter = sub_clause.get("letter", "")
                sub_clause_text = sub_clause.get("text", "")

                rag_data.append({
                    "id": f"{article_id}.{clause_number}{sub_clause_letter}",
                    "article": article_id,
                    "clause": f"{clause_number}{sub_clause_letter}",
                    "title": article_title,
                    "text": sub_clause_text,
                    "context": general_context
                })

    return rag_data


def save_rag_json(parsed_data, output_path):
    """
    Saves the RAG-ready JSON to a file.
    Args:
        parsed_data (dict): Parsed law data.
        output_path (str): File path to save the RAG JSON.
    """
    rag_ready_data = convert_to_rag_format(parsed_data)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(rag_ready_data, json_file, ensure_ascii=False, indent=4)
    print(f"RAG-ready JSON saved to {output_path}")


# Example usage:
input_json_file = "luat_viet_nam.json"  # Path to the parsed law JSON
output_rag_file = "rag_format.json"  # Output path for RAG-ready JSON

# Read the parsed law data from JSON
with open(input_json_file, "r", encoding="utf-8") as json_file:
    law_data = json.load(json_file)

# Save the RAG JSON version
save_rag_json(law_data, output_rag_file)