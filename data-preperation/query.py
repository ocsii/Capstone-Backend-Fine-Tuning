from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
import faiss
import numpy as np

# Step 1: Load models and FAISS index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
index = faiss.read_index("handbook_index.faiss")

def query_faiss_index(query, top_k=5):
    """Search the FAISS index for the top-k closest matches."""
    query_embedding = sentence_model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

def re_rank_results(query, retrieved_sections):
    """Re-rank the retrieved sections using a cross-encoder."""
    pairs = [[query, section] for section in retrieved_sections]
    scores = cross_encoder.predict(pairs)
    best_match_index = scores.argmax()
    return retrieved_sections[best_match_index]  # Return the best-matching section

def extract_answer(query, context):
    """Extract the most relevant sentence or phrase using a QA model."""
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

    # Step 3: Re-rank the sections for better relevance
    best_section = re_rank_results(query, retrieved_sections)

    # Step 4: Extract the most relevant sentence or phrase
    extracted_answer = extract_answer(query, best_section)

    # Step 5: Generate a human-like response (Optional)
    final_response = f"Based on the handbook: {extracted_answer}"
    return final_response

# Example usage
if __name__ == "__main__":
    query = "Is Software Engineering counted in honours?"
    response = generate_response(query)
    print(response)


# GPT
# It is working somewhat, however, the replies are kinda short. Like if I ask (What is the subject code and credit value for Networking Principles) it just replies (net1024). How do I make it better?
# Another example is when I ask "What is the learning Outcomes for Malay Langauge I get ("seletah tamat kursus ini") and this is the original text (Learning outcomes: Setelah tamat kursus ini pelajar dapat • Menerangkan kandungan teks penuh yang menggunakan ayat mudah dan ayat berlapis • Bertutur dalam pelbagai situasi dengan menggunakan ayat mudah dan ayat berlapis • menyusun idea secara kreatif dan sistematik dalam penulisan karangan pendek)"
# Also, when asking "What is the pre-requisite for Object Oriented Programming" I get "credit value: 4. learning outcomes" which is clearly wrong. I think it says this beacuse on top of the text, there is this "subject name: object oriented programming. subject code: prg 2104. credit value: 4. learning outcomes:, however, the text the answer is taken form is all the way down below in the last paragraph. I assume the ranking is wrong?"