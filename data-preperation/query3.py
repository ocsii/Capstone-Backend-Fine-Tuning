from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
import faiss
import numpy as np

# Step 1: Load models and FAISS index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
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

def generate_summarized_response(query, top_sections):
    """Generate a focused, human-like response using T5."""
    # Join the top sections into a single context
    context = " ".join(top_sections)

    # Create a more focused prompt for T5
    input_text = f"Answer the following question using only relevant details.\n\nQuestion: {query}\nContext: {context}"

    # Generate the summary with a higher max_length for more complete answers
    summary = summarizer(input_text, max_length=300, truncation=True)[0]['summary_text']

    return summary


def generate_response(query):
    """Orchestrate the retrieval, re-ranking, and summarization-based response generation."""
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

    # Step 4: Use the top 3 sections for the final summarized response
    top_sections = [section for _, section in ranked_sections[:3]]
    final_response = generate_summarized_response(query, top_sections)

    return final_response

# Example usage
if __name__ == "__main__":
    query = "Is software engineering counted in honours?"
    response = generate_response(query)
    print("Answer: " + response)


