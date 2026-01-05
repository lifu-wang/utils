import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# 1. HARDWARE FIXES (Blackwell GB10 + ARM64)
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 2. CONFIGURATION
model_id = "unsloth/meta-llama-3.1-8b-instruct-bnb-4bit"
dataset_file = "data/kernel_code_clean.jsonl"

# 3. LOAD TOKENIZER & MODEL
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16, # Optimized for Blackwell
    bnb_4bit_use_double_quant=True,
)

print(f"📥 Loading {model_id}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# 4. PREPARE LORA
model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 5. DATASET LOADING
dataset = load_dataset("json", data_files={"train": dataset_file}, split="train")

# 6. SFT CONFIGURATION (Updated for 2026 API)
sft_config = SFTConfig(
    output_dir="./outputs_vanilla",
    dataset_text_field="response",   # The column in your JSONL
    max_length=4096,                # FIX: Renamed from max_seq_length
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    bf16=True,                      # Use Blackwell's native precision
    logging_steps=1,
    max_steps=500,
    save_strategy="steps",
    save_steps=100,
    report_to="none"
)

# 7. TRAINER INITIALIZATION
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    args=sft_config,
    processing_class=tokenizer,     # New standard replacing 'tokenizer'
)

# 8. EXECUTE
print("🚀 Starting Training on GB10...")
trainer.train()

# 9. SAVE
model.save_pretrained("./model_kernel_vanilla")
print("✅ Training Complete. Model saved to ./model_kernel_vanilla")

