import torch
import os
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Paths for the merge process
# We use the full unsloth/meta-llama-3.1-8b-instruct to get 16-bit weights
base_model_id = "unsloth/meta-llama-3.1-8b-instruct" 
adapter_path = "./model_kernel_vanilla"
output_path = "./merged_kernel_expert"

def main():
    # 1. Load the Tokenizer
    print(f"📥 Loading tokenizer for {base_model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)

    # 2. Load the Base Model in FP16
    # This will load the full 16-bit weights into VRAM/System RAM
    print(f"📥 Loading Base Model in Float16 (FP16) precision...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16, 
        device_map="auto",
        trust_remote_code=True
    )

    # 3. Load and Attach the Trained Adapters
    print(f"🧠 Attaching adapters from {adapter_path}...")
    model = PeftModel.from_pretrained(base_model, adapter_path)

    # 4. Merge the Weights
    # This step fuses the adapter logic into the base model parameters
    print("🔗 Fusing LoRA adapters into base model weights...")
    merged_model = model.merge_and_unload()

    # 5. Save the Merged Expert Model
    print(f"💾 Saving merged model to {output_path}...")
    # Standard safetensors format is best for llama.cpp compatibility
    merged_model.save_pretrained(
        output_path, 
        safe_serialization=True,
        max_shard_size="5GB"
    )
    tokenizer.save_pretrained(output_path)

    print("\n✅ SUCCESS!")
    print(f"Final FP16 model saved in: {output_path}")
    print(f"Next step: Verify size with 'du -sh {output_path}' (Should be ~15-16GB)")

if __name__ == "__main__":
    main()
