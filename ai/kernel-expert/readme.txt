📜 Project Blueprint: The Hybrid Kernel Expert

The goal was to create an AI that combines Parametric Knowledge (Fine-tuned intuition on Kernel C patterns) with Non-Parametric Facts (Real-time RAG retrieval from source headers and documentation).
🏗️ Phase 1: Environment & Infrastructure

The foundational challenge was aligning modern LLM libraries with the sm_121 (Blackwell) architecture and aarch64 CPU.

Setup Steps:
Bash

# 1. System Dependencies
sudo apt update && sudo apt install -y build-essential cmake ctags libcurl4-openssl-dev

# 2. Virtual Environment
python3 -m venv ~/py311
source ~/py311/bin/activate

# 3. Blackwell-Optimized PyTorch (Nightly for CUDA 12.x/13.0 support)
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

# 4. LLM Stack
pip install transformers peft trl bitsandbytes accelerate datasets chromadb ollama

⛏️ Phase 2: Data Engineering (Miner & Curator)

We transformed 259MB of raw Linux Source into a high-density training set of 11,000+ logic-rich functions.

Key Scripts:

    The Miner: Uses ctags to extract function scopes.

    The Curator: Filters for complexity (functions > 10 lines) to avoid training on "boilerplate."

Data Curator
Jan 5, 3:01 PM

🚀 Phase 3: Fine-Tuning (The Blackwell Pivot)

We initially attempted Unsloth, but it failed because its Triton kernels were not yet pre-compiled for Blackwell (sm_121). We pivoted to a Vanilla SFT approach.
Component	Choice	Reason
Base Model	Llama-3.1-8B-Instruct	Superior reasoning & large context window.
Precision	Bfloat16 (BF16)	Native Blackwell support; prevents gradient overflow.
Technique	QLoRA (4-bit)	Fits training in < 16GB VRAM while preserving logic.
🔗 Phase 4: Merging & Quantization

To move to production (Ollama), we had to fuse the "Delta Brain" (LoRA) back into the "Original Brain."

1. The FP16 Merge: (Must result in a ~15GB folder)
🧠 Phase 5: Hybrid RAG Integration

This final phase connects the fine-tuned model to the ChromaDB vector store containing 11,167 indexed files.
