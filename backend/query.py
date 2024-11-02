from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
from openai import OpenAI
import os


# Step 1: Load models and FAISS index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
index = faiss.read_index("C:/Users/chris/Desktop/CP2/Fine Tuning BERT/backend/datasets/combined.faiss")

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

def call_openai_gpt(query, top_sections):
    section1 = top_sections[0] if len(top_sections) > 0 else ""
    section2 = top_sections[1] if len(top_sections) > 1 else ""
    section3 = top_sections[2] if len(top_sections) > 2 else ""

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": (
                "You are a helpful assistant. Your job is to answer the query using the provided sections. "
                "Always search for the answer in **Section 1** first. If the answer is not found there, then refer to Section 2. "
                "If still not found, refer to Section 3. If the answer cannot be found in any section, answer based on closest match from the text."

            )},
            {"role": "user", "content": f"Query: {query}\n"},
            {"role": "user", "content": f"Section 1: {section1}\n"},
            {"role": "user", "content": f"Section 2: {section2}\n"},
            {"role": "user", "content": f"Section 3: {section3}\n"}
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion

def generate_response_with_gpt(query):
    # Query FAISS and re-rank sections
    distances, indices = query_faiss_index(query)
    with open('C:/Users/chris/Desktop/CP2/Fine Tuning BERT/backend/datasets/combined.txt', 'r', encoding='utf-8') as f:
        sections = [line.strip() for line in f if line.strip()]
    
    retrieved_sections = [sections[idx] for idx in indices[0]]
    ranked_sections = re_rank_results(query, retrieved_sections)

    # Get the top 3 sections and call GPT
    top_sections = [section for _, section in ranked_sections[:3]]
    gpt_response = call_openai_gpt(query, top_sections)

    # Extract the content of the answer from the response
    answer_content = gpt_response.choices[0].message.content  

    for section in top_sections:
        print(section + "\n\n\n")

    return f"Answer: {answer_content}"  # Return only the answer content

# Example usage
if __name__ == "__main__":

    query = "What is the criteria for first class honors?"
    response = generate_response_with_gpt(query)
    print(response)
