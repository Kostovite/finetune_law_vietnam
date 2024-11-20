# Install required libraries
# pip install faiss-cpu transformers datasets peft accelerate

import json
import os
import faiss
import numpy as np
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model
import torch
torch.cuda.empty_cache()

# 1. Load the RAG corpus
def load_rag_corpus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Dataset.from_list(data)

# 2. Index the corpus with FAISS
def build_faiss_index(dataset, embedding_model, tokenizer):
    print("Building FAISS index...")
    # Convert texts to embeddings
    corpus_embeddings = []
    for record in dataset:
        text = record['text']
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(embedding_model.device)
        with torch.no_grad():
            embeddings = embedding_model(**inputs, output_hidden_states=True).hidden_states[-1][:, 0, :].cpu().numpy()
        corpus_embeddings.append(embeddings)

    # Build FAISS index
    index = faiss.IndexFlatL2(embedding_model.config.hidden_size)  # Adjust dimensions to match embedding size
    index.add(np.vstack(corpus_embeddings))
    return index

# 3. Retrieve relevant chunks
def retrieve(query, index, dataset, embedding_model, tokenizer, top_k=5):
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True).to(embedding_model.device)
    with torch.no_grad():
        query_embedding = embedding_model(**inputs, output_hidden_states=True).hidden_states[-1][:, 0, :].cpu().numpy()
    
    distances, indices = index.search(query_embedding, top_k)
    results = [dataset[int(i)] for i in indices[0]]
    return results

# 4. Main function
def main():
    # Paths
    json_path = "rag_corpus.json"  # Replace with your RAG JSON file
    alpaca_path = "alpaca_format.json"  # Replace with your Alpaca dataset file

    # Check if files exist
    if not os.path.exists(json_path) or not os.path.exists(alpaca_path):
        print(f"Error: Required files not found.")
        return

    # Load RAG corpus
    print("Loading RAG corpus...")
    rag_dataset = load_rag_corpus(json_path)

    # Load Alpaca dataset
    print("Loading Alpaca dataset...")
    with open(alpaca_path, "r") as f:
        alpaca_data = json.load(f)

    # Load the Qwen model and tokenizer
    model_name = "Qwen/Qwen2.5-0.5B"
    print("Loading model and tokenizer...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model = torch.nn.DataParallel(model, device_ids=[0, 1])
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    # Configure LoRA for PEFT
    print("Configuring LoRA...")
    config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )
    peft_model = get_peft_model(model, config)

    # Build FAISS index
    index = build_faiss_index(rag_dataset, model, tokenizer)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./qwen_finetuned_rag",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        evaluation_strategy="steps",
        logging_steps=500,
        save_steps=1000,
        save_total_limit=2,
        learning_rate=5e-5,
        num_train_epochs=3,
        weight_decay=0.01,
        fp16=True,
        gradient_accumulation_steps=8,
        max_grad_norm=1.0,
        push_to_hub=False,
        dataloader_num_workers=2,
        run_name="qwen_rag_training_run",
        load_best_model_at_end=True,
    )

    # Tokenize and retrieve context for Alpaca data
    print("Retrieving and tokenizing Alpaca data...")
    tokenized_dataset = []
    for entry in alpaca_data:
        query = entry['instruction']
        if entry['input']:
            query += f"\nInput: {entry['input']}"

        # Retrieve relevant documents
        retrieved_docs = retrieve(query, index, rag_dataset, model, tokenizer)
        context = "\n".join([doc['text'] for doc in retrieved_docs])

        # Combine context with prompt
        prompt_with_context = f"Context:\n{context}\n\nQuery:\n{query}"
        tokenized_dataset.append({
            "input_ids": tokenizer(
                prompt_with_context,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=512
            )["input_ids"],
            "labels": tokenizer(
                entry["output"],
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=512
            )["input_ids"],
        })

    # Initialize the data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

    # Train the model
    print("Starting training...")
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    print("Training the model...")
    trainer.train()

    # Save the model and tokenizer
    print("Saving model and tokenizer...")
    trainer.save_model("./qwen_finetuned_rag")
    tokenizer.save_pretrained("./qwen_finetuned_rag")

# Run the main function
if __name__ == "__main__":
    main()