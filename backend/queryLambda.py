from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
import requests



# Step 1: Load models and FAISS index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
index = faiss.read_index("C:/Users/chris/Desktop/CP2/Fine Tuning BERT/backend/data-preparation/datasets/text-faiss/combined.faiss")
LAMBDA_API_URL = "https://wvleewwlcmkv6yjxhzyl27fxjq0qzmws.lambda-url.ap-southeast-1.on.aws/"



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

def call_openai_api(query, top_sections):
    payload = {
        "query": query,
        "retrieved_sections": top_sections  
    }

    try:
        response = requests.post(LAMBDA_API_URL, json=payload)
        response_data = response.json()
        return response_data.get("answer")
    except Exception as e:
        print("Error calling OpenAI GPT:", str(e))
        return "Error fetching response."



def generate_response_with_gpt(query):
    # Query FAISS and re-rank sections
    distances, indices = query_faiss_index(query)
    
    with open('C:/Users/chris/Desktop/CP2/Fine Tuning BERT/backend/data-preparation/datasets/text-manually-updated/combined.txt', 'r', encoding='utf-8') as f:
        sections = [line.strip() for line in f if line.strip()]
    
    retrieved_sections = [sections[idx] for idx in indices[0]]
    ranked_sections = re_rank_results(query, retrieved_sections)

    # Get the top 3 sections and call GPT
    top_sections = [section for _, section in ranked_sections[:3]]
    gpt_response = call_openai_api(query, top_sections)

    return f"Answer: {gpt_response}"  # Return only the answer content

# Example usage
if __name__ == "__main__":

    query = "What is the criteria for first class honors"
    response = generate_response_with_gpt(query)
    print(response)
