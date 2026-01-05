import os
import subprocess
import json
import re

BASE_DIR = "/home/lifu/llm-kernel"
SOURCE_DIR = os.path.join(BASE_DIR, "linux_pruned")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "kernel_train.jsonl")

def extract_functions():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"🔍 Scanning {SOURCE_DIR}...")

    try:
        # Using -x for name, kind, line, file, content
        result = subprocess.run(
            ["ctags", "-R", "-x", "--c-kinds=f", SOURCE_DIR],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ ctags failed: {e}")
        return

    lines = result.stdout.splitlines()
    dataset = []
    print(f"📂 Found {len(lines)} potential functions. Extracting...")

    for line in lines:
        # Regex to find the first integer in the line - this is our line number
        match = re.search(r'\s+(\d+)\s+', line)
        if not match: continue
        
        start_line = int(match.group(1))
        # Split line to get name (index 0) and file path
        parts = line.split()
        func_name = parts[0]
        
        # Find the part that looks like a file path (contains / or .c)
        file_path = None
        for p in parts:
            if "/" in p or p.endswith(".c") or p.endswith(".h"):
                if os.path.exists(p):
                    file_path = p
                    break
        
        if not file_path: continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as src:
                all_lines = src.readlines()
                body = []
                # Simple kernel brace matching
                for i in range(start_line - 1, len(all_lines)):
                    l = all_lines[i]
                    body.append(l)
                    if l.startswith('}') or (l.strip() == '}' and i > start_line):
                        break
                
                if body:
                    dataset.append({
                        "instruction": f"Explain or implement the Linux kernel function '{func_name}'",
                        "context": f"File: {os.path.relpath(file_path, SOURCE_DIR)}",
                        "response": "".join(body)
                    })
        except:
            continue
        
        if len(dataset) % 5000 == 0:
            print(f"Processed {len(dataset)} pairs...")

    with open(OUTPUT_FILE, 'w') as out:
        for entry in dataset:
            out.write(json.dumps(entry) + '\n')
    
    print(f"✅ Success! Final count: {len(dataset)} training pairs.")

if __name__ == "__main__":
    extract_functions()
