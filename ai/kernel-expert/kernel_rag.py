import os
import ollama
import chromadb
from chromadb.utils import embedding_functions

# --- CONFIGURATION ---
# Everything is relative to ~/llm-kernel
DB_PATH = "./kernel_vector_db"
# We now search both Documentation (for explanations) and include (for API definitions)
SEARCH_PATHS = [
    "./linux_pruned/Documentation",
    "./linux_pruned/include"
]
MODEL_NAME = "kernel-expert"

# 1. INITIALIZE VECTOR DATABASE
# ChromaDB stores the "embeddings" (mathematical maps) of your kernel files
client = chromadb.PersistentClient(path=DB_PATH)

# Using a standard local embedding model (runs locally on your CPU/GPU)
emb_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(
    name="linux_kernel_knowledge", 
    embedding_function=emb_func
)

# 2. INGESTION LOGIC
def ingest_kernel_resources(paths):
    """
    Scans the provided folders and adds text/code files to the vector store.
    """
    count = 0
    for path in paths:
        if not os.path.exists(path):
            print(f"⚠️ Warning: Path not found: {path}")
            continue
            
        print(f"📂 Starting ingestion from {path}...")
        for root, dirs, files in os.walk(path):
            for file in files:
                # We index text, restructured text, and C header files
                if file.endswith((".txt", ".rst", ".h", ".c")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if len(content.strip()) < 50: continue # Skip tiny/empty files
                            
                            collection.add(
                                documents=[content],
                                ids=[file_path],
                                metadatas=[{"source": file_path, "filename": file}]
                            )
                            count += 1
                            if count % 100 == 0:
                                print(f"✅ Indexed {count} files...")
                    except Exception as e:
                        print(f"⚠️ Could not read {file}: {e}")
    
    print(f"🚀 Ingestion complete. Total {count} documents in {DB_PATH}.")

# 3. HYBRID QUERY ENGINE
def ask_kernel_expert(question):
    """
    The Hybrid Loop: 
    1. Retrieve specific facts from ChromaDB (RAG)
    2. Feed facts + question to the Fine-Tuned Model (SFT)
    """
    # Search for the top 5 most relevant snippets
    # The GB10 can handle large context windows easily
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    # Combine retrieved segments into a context string
    context_chunks = results['documents'][0]
    context_str = "\n\n---\n\n".join(context_chunks)
    sources = [m['source'] for m in results['metadatas'][0]]

    # Build the Hybrid Prompt
    # This forces the model to use the retrieved files as 'Ground Truth'
    prompt = f"""
    SYSTEM: You are the Linux Kernel Expert. Use the PROVIDED CONTEXT as the primary source of truth.
    If the context is insufficient, fall back to your specialized fine-tuned knowledge.
    
    CONTEXT FROM KERNEL SOURCE:
    {context_str}
    
    USER QUESTION:
    {question}
    
    RESPONSE (Kernel C style, tab-indented):
    """

    print("🧠 Querying Hybrid Brain (RAG + Fine-Tuned Expert)...")
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)
    
    return {
        "answer": response['response'],
        "sources": sources
    }

# --- EXECUTION ---
if __name__ == "__main__":
    # If database is empty, start the one-time ingestion process
    if collection.count() == 0:
        ingest_kernel_resources(SEARCH_PATHS)
    else:
        print(f"ℹ️ Vector DB found with {collection.count()} documents. Skipping ingestion.")
    
    # Example Session
    print("\n--- KERNEL EXPERT TERMINAL ---")
    while True:
        user_input = input("\n[Q]: ")
        if user_input.lower() in ['exit', 'quit']: break
        
        result = ask_kernel_expert(user_input)
        
        print("\n" + "—"*50)
        print(result['answer'])
        print("—"*50)
        print("\nSOURCES CONSULTED:")
        for s in result['sources']:
            print(f" 📑 {s}")
