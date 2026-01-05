from datasets import load_dataset
import os

BASE_DIR = "/home/lifu/llm-kernel"
DATA_PATH = os.path.join(BASE_DIR, "data/kernel_code_clean.jsonl")

# 1. Physical check
if not os.path.exists(DATA_PATH):
    print(f"❌ File not found at {DATA_PATH}")
else:
    print(f"✅ File exists. Size: {os.path.getsize(DATA_PATH) / 1024 / 1024:.2f} MB")

# 2. Load check
dataset = load_dataset("json", data_files={"train": DATA_PATH}, split="train")
print(f"📊 Number of samples in dataset: {len(dataset)}")

# 3. Format check
if len(dataset) > 0:
    print("📝 Sample 0 instruction:", dataset[0].get("instruction")[:50])
    # Check if the 'text' field was actually created by the map function
    # (Re-run your map function logic here to see if it works)
