# Install required libraries
# pip install transformers datasets peft accelerate

# Import libraries
import json
import os
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

# 1. Load the Alpaca dataset
def load_alpaca_format(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    processed_data = []
    for entry in data:
        prompt = entry['instruction']
        if entry['input']:
            prompt += f"\nInput: {entry['input']}"
        processed_data.append({
            "prompt": prompt,
            "completion": entry['output']
        })

    return Dataset.from_list(processed_data)

# 2. Main function
def main():
    # Get user input for the dataset path
    json_path = "alpaca_format.json"  # Replace with the correct path
    
    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: File '{json_path}' not found.")
        return

    # Load dataset
    print("Loading dataset...")
    alpaca_dataset = load_alpaca_format(json_path)
    alpaca_dataset = alpaca_dataset.train_test_split(test_size=0.1)

    # Load the Qwen-2.5 model and tokenizer
    model_name = "Qwen/Qwen2.5-0.5B"
    print("Loading model and tokenizer...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # model = torch.nn.DataParallel(model, device_ids=[0, 1])
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    # Tokenize the dataset
    print("Tokenizing dataset...")
    def tokenize_function(example):
        # Tokenize with truncation and padding
        tokenized = tokenizer(
            example["prompt"],
            text_target=example["completion"],
            truncation=True,
            padding="max_length",  # Pad sequences to the same length
            max_length=512,  # Adjust based on model's context length
        )
        return tokenized

    tokenized_dataset = alpaca_dataset.map(tokenize_function, batched=True)

    # Configure LoRA for PEFT
    print("Configuring LoRA...")
    config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],  # Adjust based on Qwen layers
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )
    peft_model = get_peft_model(model, config)

    training_args = TrainingArguments(
        output_dir="./qwen_finetuned",
        per_device_train_batch_size=1,  # Reduced batch size
        per_device_eval_batch_size=1,   # Reduced evaluation batch size
        evaluation_strategy="steps",
        logging_steps=500,
        save_steps=1000,
        save_total_limit=2,
        learning_rate=5e-5,
        num_train_epochs=3,
        weight_decay=0.01,
        fp16=True,  # Enable mixed precision
        gradient_accumulation_steps=8,  # Accumulate gradients to simulate a larger batch
        max_grad_norm=1.0,
        push_to_hub=False,
        dataloader_num_workers=2,  # Reduce number of workers
        run_name="qwen_training_run",
        load_best_model_at_end=True,
    )

    # Initialize the data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

    # Initialize and train the model
    print("Starting training...")
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,  # Include data collator here
    )

    print("Training the model...")
    trainer.train()
    # Save the fine-tuned model and tokenizer
    print("Saving model and tokenizer...")
    trainer.save_model("./qwen_finetuned")
    tokenizer.save_pretrained("./qwen_finetuned")

    # (Optional) Evaluate with a sample input
    print("Evaluating a sample input...")
    test_prompt = "[khoản 42] [Điều 2] gồm có gì?"
    inputs = tokenizer(test_prompt, return_tensors="pt").to(peft_model.device)

    # Set pad_token to eos_token to avoid padding issues
    tokenizer.pad_token = tokenizer.eos_token
    peft_model.config.pad_token_id = tokenizer.eos_token_id

    # Generate output with sampling and avoid repetition
    outputs = peft_model.generate(
        **inputs, 
        max_new_tokens=100, 
        do_sample=True,  # Enable sampling
        top_k=50,        # Top-k sampling (limit to top 50 tokens)
        top_p=0.95,      # Nucleus sampling (limit to 95% cumulative probability)
        temperature=0.9  # Controls randomness (lower = more deterministic)
    )

    print("Generated Output:", tokenizer.decode(outputs[0], skip_special_tokens=True))

# Run the main function
if __name__ == "__main__":
    main()