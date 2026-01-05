import json
import os

BASE_DIR = "/home/lifu/llm-kernel"
INPUT_FILE = os.path.join(BASE_DIR, "data/kernel_train.jsonl")
OUTPUT_CODE = os.path.join(BASE_DIR, "data/kernel_code_clean.jsonl")
OUTPUT_DOCS = os.path.join(BASE_DIR, "data/kernel_docs_rag.jsonl")

def filter_data():
    code_count = 0
    doc_count = 0
    
    with open(INPUT_FILE, 'r') as f, \
         open(OUTPUT_CODE, 'w') as f_code, \
         open(OUTPUT_DOCS, 'w') as f_docs:
        
        for line in f:
            data = json.loads(line)
            context = data.get("context", "")
            response = data.get("response", "")
            
            # Identify Documentation vs Code
            if ".rst" in context or ".txt" in context or "Documentation/" in context:
                f_docs.write(line)
                doc_count += 1
            elif context.endswith(".c"):
                # Only keep substantial functions (> 10 lines)
                if response.count('\n') > 10:
                    f_code.write(line)
                    code_count += 1
            else:
                # Catch-all for headers or other files
                f_docs.write(line)

    print(f"✅ Filtered Results:")
    print(f"   - Clean C Functions (LoRA target): {code_count}")
    print(f"   - Documentation/Headers (RAG target): {doc_count}")

if __name__ == "__main__":
    filter_data()
