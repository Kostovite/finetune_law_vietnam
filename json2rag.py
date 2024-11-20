import json

def convert_to_rag_format(input_data):
    """
    Converts nested JSON structure to a flat RAG-ready format.
    Args:
        input_data (dict): The original nested JSON data.
    Returns:
        list: A list of dictionaries in RAG format.
    """
    rag_data = []

    # Extract header for general context (optional, can add metadata here if needed)
    header = " ".join(input_data.get("header", []))

    for chapter in input_data.get("content", []):
        chapter_name = chapter.get("chuong", "")

        for section in chapter.get("muc", []):
            for article in section.get("dieu", []):
                article_id = article.get("id", "")
                article_title = article.get("title", "")
                
                for clause in article.get("content", []):
                    clause_number = clause.get("number", "")
                    clause_text = clause.get("text", "")
                    sub_clauses = clause.get("sub_clauses", [])
                    
                    # Add the main clause
                    rag_data.append({
                        "id": f"{article_id}.{clause_number}",
                        "chapter": chapter_name,
                        "article": article_id,
                        "clause": clause_number,
                        "title": article_title,
                        "text": clause_text
                    })

                    # Add any sub-clauses
                    for sub_clause in sub_clauses:
                        sub_clause_letter = sub_clause.get("letter", "")
                        sub_clause_text = sub_clause.get("text", "")
                        rag_data.append({
                            "id": f"{article_id}.{clause_number}{sub_clause_letter}",
                            "chapter": chapter_name,
                            "article": article_id,
                            "clause": f"{clause_number}{sub_clause_letter}",
                            "title": article_title,
                            "text": sub_clause_text
                        })
    
    return rag_data


# Example usage
if __name__ == "__main__":
    # Load your nested JSON file
    input_file = "luat_viet_nam.json"  # Replace with your input file name
    output_file = "rag_ready_data.json"  # Replace with your output file name

    with open(input_file, "r", encoding="utf-8") as infile:
        nested_data = json.load(infile)

    # Convert to RAG format
    rag_ready_data = convert_to_rag_format(nested_data)

    # Save to output JSON
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(rag_ready_data, outfile, ensure_ascii=False, indent=4)

    print(f"Conversion complete! RAG-ready data saved to {output_file}.")