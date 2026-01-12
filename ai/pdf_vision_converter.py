import sys
import io
import ollama
from pdf2image import convert_from_path

def process_pdf(pdf_path):
    print(f"Processing {pdf_path}...")
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        print("Ensure poppler is installed: 'brew install poppler'")
        return

    full_text = []

    for i, image in enumerate(images):
        print(f"  - Page {i+1}/{len(images)}: Analyzing with llama3.2-vision...")
        
        # Save image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Send to Ollama Vision
        try:
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[{
                    'role': 'user',
                    'content': 'Analyze this image detailedly. Extract all text. If there are graphs, diagrams, or charts, explain their meaning, axes, trends, and data points fully.',
                    'images': [img_bytes]
                }]
            )
            description = response['message']['content']
            full_text.append(f"--- Page {i+1} Start ---\n{description}\n--- Page {i+1} End ---\n")
            
        except Exception as e:
            print(f"    Error calling Ollama: {e}")

    # Save to .txt file
    output_filename = f"{pdf_path}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))
    print(f"  -> Success! Saved descriptions to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_vision_converter.py <file.pdf>")
    else:
        for f in sys.argv[1:]:
            process_pdf(f)
