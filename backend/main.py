from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
import requests
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

""" This is the backend used to host on Render (free tier) """

# Paths
base_path = os.path.dirname(os.path.abspath(__file__))
faiss_path = os.path.join(base_path, 'datasets/combined.faiss')
txt_path = os.path.join(base_path, 'datasets/combined.txt')
LAMBDA_API_URL = "https://wvleewwlcmkv6yjxhzyl27fxjq0qzmws.lambda-url.ap-southeast-1.on.aws/"


# Load modeel info faiss index
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 
index = faiss.read_index(faiss_path)

app = FastAPI()

# CORS settings for local setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class Query(BaseModel):
    question: str

# Using CRON job to ping this endpoint to keep Render backend running
@app.get("/health")
async def health_check():
    return {"status": "up"}


@app.post("/query")
async def query_faiss(query: Query):
    response = generate_response_with_gpt(query.question)
    return {"answer": response}
    

def query_faiss_index(query, top_k=10):
    #Search the FAISS index for the top-k closest matches
    query_embedding = sentence_model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, indices = index.search(query_embedding, top_k)

    return distances, indices


#Re-rank the retrieved sections using a cross-encoder and return scores
def re_rank_results(query, retrieved_sections):

    # Create pairs with (query + section)
    pairs = [[query, section] for section in retrieved_sections]

    # Predict relevance for each pair
    scores = cross_encoder.predict(pairs)
    
    # Comibine scores and section into suples and sort (first element of the tuple: specified by key=lambda)
    ranked_sections = sorted(zip(scores, retrieved_sections), key=lambda x: x[0], reverse=True)
    
    return ranked_sections


# Change to model gpt-4o before submit
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
    # Distances - similarity scores
    # indices - indices pointing to the most relevant items in the dataset
    distances, indices = query_faiss_index(query)
    
    # Retrieve sections (only no empty lines) and remove whitespace
    with open(txt_path, 'r', encoding='utf-8') as f:
        sections = [line.strip() for line in f if line.strip()]
    
    # Search the txt file based on sections in indices top returned list [0]
    retrieved_sections = [sections[idx] for idx in indices[0]]

    # Rerank and sort sections
    ranked_sections = re_rank_results(query, retrieved_sections)

    # Take only top 3 sections
    top_sections = [section for _, section in ranked_sections[:5]]

    # Send query and top 3 sections to GPT API
    gpt_response = call_openai_api(query, top_sections)

    return gpt_response 

# Main function (not used unless run manually)
if __name__ == "__main__":

    query = "What is the criteria for first class honors"
    response = generate_response_with_gpt(query)
    print(response)
