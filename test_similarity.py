import os
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

sentence_a = "What is the internship duration?"
sentence_b = "How many weeks does the internship last?"
sentence_c = "What are the hostel fees?"

print("Generating embeddings...")

def get_embedding(text):
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=text
    )
    return response.embeddings[0].values

vec_a = np.array(get_embedding(sentence_a))
vec_b = np.array(get_embedding(sentence_b))
vec_c = np.array(get_embedding(sentence_c))

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

sim_a_b = cosine_similarity(vec_a, vec_b)
sim_a_c = cosine_similarity(vec_a, vec_c)

print("\n--- Similarity Scores ---")
print(f"1. '{sentence_a}' vs '{sentence_b}'")
print(f"   Score: {sim_a_b:.4f}\n")
print(f"2. '{sentence_a}' vs '{sentence_c}'")
print(f"   Score: {sim_a_c:.4f}\n")
