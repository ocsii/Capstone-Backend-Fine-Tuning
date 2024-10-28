import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def generate_embeddings_from_file(input_file='lowercase_handbook.txt', index_file='handbook_index.faiss'):
    """Generate embeddings for the preprocessed text and save them to a FAISS index."""
    # Load the pre-trained model for generating embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Read the preprocessed text and split it into chunks
    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = [line.strip() for line in f if line.strip()]

    # Generate embeddings for each chunk
    embeddings = model.encode(chunks, convert_to_tensor=True)

    # Save the embeddings to a FAISS index
    save_to_faiss(embeddings, index_file)
    print(f"FAISS index saved to {index_file}")

def save_to_faiss(embeddings, index_file):
    """Save the generated embeddings to a FAISS index."""
    dimension = embeddings.shape[1]  # Get embedding dimension
    index = faiss.IndexFlatL2(dimension)  # Create a FAISS index with L2 distance
    index.add(embeddings.cpu().numpy())  # Add all embeddings to the index
    faiss.write_index(index, index_file)  # Save the index to disk

# Run the embedding generation function
if __name__ == "__main__":
    generate_embeddings_from_file()
