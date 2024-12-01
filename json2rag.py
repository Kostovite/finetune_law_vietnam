import os
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
                # Uncomment the next line if you need general context
                # "context": general_context
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
                    # Uncomment the next line if you need general context
                    # "context": general_context
                })

    return rag_data


def convert_folder_to_rag(input_folder, output_folder):
    """
    Converts all JSON files in the input folder to RAG-ready format and saves in the output folder.
    Args:
        input_folder (str): Path to the folder containing parsed law JSON files.
        output_folder (str): Path to the folder to save RAG-ready JSON files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_name = file_name  # Keep the same file name
            output_file_path = os.path.join(output_folder, output_file_name)

            try:
                # Load parsed law JSON
                with open(input_file_path, "r", encoding="utf-8") as json_file:
                    parsed_data = json.load(json_file)

                # Convert to RAG-ready format
                rag_ready_data = convert_to_rag_format(parsed_data)

                # Save RAG JSON
                with open(output_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(rag_ready_data, json_file, ensure_ascii=False, indent=4)
                print(f"Processed and saved RAG format: {output_file_path}")
            except Exception as e:
                print(f"Failed to process {input_file_path}: {e}")


# Example usage
input_folder = "Vietnam-Law-tree_json"
output_folder = "Vietnam-Law-rag_json"
convert_folder_to_rag(input_folder, output_folder)