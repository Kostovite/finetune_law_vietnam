import json

def convert_to_rag_format(input_data):
    """
    Converts flattened JSON structure (Điều-focused) to a flat RAG-ready format.
    Args:
        input_data (dict): The original flattened JSON data with header, footer, and Điều structure.
    Returns:
        list: A list of dictionaries in RAG format.
    """
    rag_data = []

    # Extract the header as general context
    header = " ".join(input_data.get("header", []))
    footer = " ".join(input_data.get("footer", []))  # Capture footer for additional context

    for article in input_data.get("content", []):
        article_id = article.get("id", "")
        article_title = article.get("title", "")
        
        for clause in article.get("content", []):
            clause_number = clause.get("number", "")
            clause_text = clause.get("text", "")
            sub_clauses = clause.get("sub_clauses", [])
            
            # Add the main clause
            rag_data.append({
                "id": f"{article_id}.{clause_number}",
                "article": article_id,
                "clause": clause_number,
                "title": article_title,
                "text": clause_text,
                "context": header  # Include header as context
            })

            # Add any sub-clauses
            for sub_clause in sub_clauses:
                sub_clause_letter = sub_clause.get("letter", "")
                sub_clause_text = sub_clause.get("text", "")
                rag_data.append({
                    "id": f"{article_id}.{clause_number}{sub_clause_letter}",
                    "article": article_id,
                    "clause": f"{clause_number}{sub_clause_letter}",
                    "title": article_title,
                    "text": sub_clause_text,
                    "context": header  # Include header as context
                })

    # Optionally, append the footer as a separate entry if required
    if footer:
        rag_data.append({
            "id": "footer",
            "article": None,
            "clause": None,
            "title": "Footer",
            "text": footer,
            "context": header  # Include header as context for consistency
        })

    return rag_data


# Example usage
if __name__ == "__main__":
    # Load your flattened JSON file
    input_file = "luat_viet_nam.json"  # Replace with your input file name
    output_file = "rag_format.json"  # Replace with your output file name

    with open(input_file, "r", encoding="utf-8") as infile:
        flattened_data = json.load(infile)

    # Convert to RAG format
    rag_ready_data = convert_to_rag_format(flattened_data)

    # Save to output JSON
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(rag_ready_data, outfile, ensure_ascii=False, indent=4)

    print(f"Conversion complete! RAG-ready data saved to {output_file}.")