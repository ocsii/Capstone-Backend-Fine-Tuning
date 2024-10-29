import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os


def generate_embeddings(input_file, index_file):
    """Generate vector embeddings and save them to FAISS index"""

    # Load pre-trained model to generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Read the manually processed text and split into chunks
    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = [line.strip() for line in f if line.strip()]

    # Generate embeddings for each chunk
    embeddings = model.encode(chunks, convert_to_tensor=True)

    # Save the embeddings to FAISS index
    save_to_faiss(embeddings, index_file)
    print(f"Done processing {input_file}, FAISS index saved to {index_file}")

def save_to_faiss(embeddings, index_file):
    """Save to .faiss"""

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.cpu().numpy())
    faiss.write_index(index, index_file)

def process_all_files(input_dir, output_dir):
    """Process all .txt files in the input directory and save their FAISS indices."""
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_dir, filename)
            index_file_name = f"{os.path.splitext(filename)[0]}.faiss"  # Create index file name
            index_file_path = os.path.join(output_dir, index_file_name)
            generate_embeddings(input_file_path, index_file_path)

if __name__ == "__main__":
    input_dir = 'data-preperation/datasets/text-manually-updated'
    output_dir = 'data-preperation/datasets/text-faiss'

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    process_all_files(input_dir, output_dir)
