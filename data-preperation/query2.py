from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
import faiss
import numpy as np

# Step 1: Load models and FAISS index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
index = faiss.read_index("handbook_index.faiss")

def query_faiss_index(query, top_k=10):
    """Search the FAISS index for the top-k closest matches."""
    query_embedding = sentence_model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

def re_rank_results(query, retrieved_sections):
    """Re-rank the retrieved sections using a cross-encoder and return scores."""
    pairs = [[query, section] for section in retrieved_sections]
    scores = cross_encoder.predict(pairs)
    
    # Sort sections by score (descending) and return all of them with scores
    ranked_sections = sorted(zip(scores, retrieved_sections), key=lambda x: x[0], reverse=True)
    
    return ranked_sections

def extract_answer(query, context):
    """Answer the query based on the infromation from the context in one sentence"""
    print(query)
    print(context)
    result = qa_pipeline(question=query, context=context)
    return result['answer']

def generate_response(query):
    """Orchestrate the retrieval, re-ranking, extraction, and final response generation."""
    # Step 1: Query FAISS index
    distances, indices = query_faiss_index(query)

    # Step 2: Retrieve sections from the preprocessed file
    with open('lowercase_handbook.txt', 'r', encoding='utf-8') as f:
        sections = [line.strip() for line in f if line.strip()]

    retrieved_sections = [sections[idx] for idx in indices[0]]

    # Step 3: Re-rank the sections and print them with scores
    ranked_sections = re_rank_results(query, retrieved_sections)

    print("Top Ranked Sections and Scores:")
    for score, section in ranked_sections:
        print(f"Score: {score:.4f}\nSection: {section}\n")

    # Step 4: Extract the most relevant sentence or phrase from the top section
    best_section = ranked_sections[0][1]  # Top-ranked section
    extracted_answer = extract_answer(query, best_section)

    # Step 5: Generate a human-like response (Optional)
    final_response = f"Based on the handbook: {extracted_answer}"
    return final_response

# Example usage
if __name__ == "__main__":
    query = "What is the pre-requisite for Internship?"
    response = generate_response(query)
    print(response)
