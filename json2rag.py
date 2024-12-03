import os
import json

def convert_to_rag_format(parsed_data, file_name):
    """
    Converts nested JSON structure into RAG-ready format with file name as ID.
    Args:
        parsed_data (dict): The parsed law data.
        file_name (str): The name of the file (used as an additional identifier).
    Returns:
        list: A list of dictionaries in RAG format.
    """
    rag_data = []

    # Build the context string (if applicable, general context is skipped here)
    
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
                "file_id": file_name  # Add the file name here
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
                    "file_id": file_name  # Add the file name here
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

                # Use file name (without extension) as the unique file_id
                base_file_name = os.path.splitext(file_name)[0]

                # Convert to RAG-ready format
                rag_ready_data = convert_to_rag_format(parsed_data, base_file_name)

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