# Install required libraries
# pip install faiss-cpu transformers datasets torch accelerate

import os
import json
import faiss
import numpy as np
import torch
import torch.nn as nn
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. Load the RAG corpus
def load_rag_corpus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Dataset.from_list(data)

# 2. Build FAISS index
def build_faiss_index(dataset, embedding_model, tokenizer):
    corpus_embeddings = []

    for i, record in enumerate(dataset):
        text = record['text']
        if not text.strip():  # Check for empty text
            print(f"Skipping empty text at index {i}.")
            continue

        # Use the model's device from embedding_model.module if it's wrapped in DataParallel
        device = embedding_model.module.device if isinstance(embedding_model, nn.DataParallel) else embedding_model.device
        
        # Tokenize and create attention mask
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        # Ensure input_ids are LongTensor and attention_mask is correctly formatted
        input_ids = input_ids.long()  # Ensure input_ids are LongTensor
        attention_mask = attention_mask.long()  # Ensure attention_mask is LongTensor

        if input_ids.size(1) == 0:  # Check if input_ids is empty
            print(f"Tokenizer produced empty input_ids for text: {text}")
            continue

        try:
            with torch.no_grad():
                # Use the model to get the embeddings
                outputs = embedding_model(input_ids, attention_mask=attention_mask, output_hidden_states=True)
                if outputs.hidden_states is None:
                    print(f"Model returned no hidden_states for text: {text}")
                    continue
                embeddings = outputs.hidden_states[-1][:, 0, :].cpu().numpy()
            corpus_embeddings.append(embeddings)
        except IndexError as e:
            print(f"Error processing text at index {i}: {text}\nError: {e}")
            continue

    if not corpus_embeddings:
        raise ValueError("No valid embeddings were generated. Please check the input data.")

    # Build FAISS index
    embedding_dim = embedding_model.config.hidden_size
    index = faiss.IndexFlatL2(embedding_dim)  # Adjust dimensions to match embedding size
    index.add(np.vstack(corpus_embeddings))
    return index

# 3. Retrieve relevant chunks
def retrieve(query, index, dataset, embedding_model, tokenizer, top_k=5):
    # Tokenize query and generate embedding
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True, max_length=512).to(embedding_model.device)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Generate query embedding
    with torch.no_grad():
        query_embedding = embedding_model(input_ids, attention_mask=attention_mask, output_hidden_states=True).hidden_states[-1][:, 0, :].cpu().numpy()

    # Perform the search in FAISS
    distances, indices = index.search(query_embedding, top_k)
    results = [dataset[int(i)] for i in indices[0]]

    # Check what is being retrieved
    print("Retrieved sections: ")
    for result in results:
        print(result['id'], result['text'])  # Ensure this matches the expected content

    return results

# 4. Generate responses using the model and retrieved context
def generate_with_rag(query, index, dataset, model, tokenizer, top_k=5, max_output_length=150):
    # Retrieve relevant context
    retrieved_docs = retrieve(query, index, dataset, model, tokenizer, top_k)
    context = "\n".join([doc['text'] for doc in retrieved_docs])

    # Add a clear instruction to generate the response in multiple languages
    prompt_with_context = f"Context:\n{context}\n\nQuery: {query}\n\nAnswer:"

    # Tokenize the prompt and ensure padding and attention_mask are included
    inputs = tokenizer(prompt_with_context, return_tensors="pt", truncation=True, padding=True, max_length=512).to(model.device)

    # Ensure pad_token_id is set if not specified
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id  # Set pad_token_id to eos_token_id if not set

    # If attention_mask is not already included, create it
    attention_mask = inputs.get('attention_mask', None)
    if attention_mask is None:
        attention_mask = torch.ones(inputs['input_ids'].shape, device=model.device)  # Set all to 1 if no mask is present

    # Generate the response with max_new_tokens instead of max_length to avoid warning
    output = model.generate(
        inputs["input_ids"],
        attention_mask=attention_mask,  # Pass attention_mask
        pad_token_id=tokenizer.pad_token_id,  # Ensure pad_token_id is passed
        max_new_tokens=150,  # Use max_new_tokens instead of max_length
        num_beams=100,  # Beam search to improve relevance
        early_stopping=True
    )

    # Decode the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return response


# 5. Main function
def main():
    # Paths
    json_path = "./finetune_law_vietnam/rag_format.json"  # Path to your RAG JSON file

    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: RAG corpus file '{json_path}' not found.")
        return

    # Load RAG corpus
    print("Loading RAG corpus...")
    rag_dataset = load_rag_corpus(json_path)

    # Load the Qwen model and tokenizer
    model_name = "Qwen/Qwen2.5-0.5B"
    print("Loading model and tokenizer...")
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # GPU setup
    if torch.cuda.is_available():
        model = model.to("cuda:0")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("No GPU detected. Using CPU.")
        model = model.to("cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    # Build FAISS index
    print("Building FAISS index...")
    index = build_faiss_index(rag_dataset, model, tokenizer)

    # Test query
    print("Testing RAG retrieval and generation...")
    test_query = "Điều 41.1:"
    response = generate_with_rag(test_query, index, rag_dataset, model, tokenizer)
    print("Generated Response:\n", response)

# Run the main function
if __name__ == "__main__":
    main()