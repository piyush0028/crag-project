import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 1. Connect to our existing database
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_collection(name="internship_knowledge")

user_question = "What happens if I miss too many classes?"
print(f"Question: '{user_question}'\n")

# 2. Convert question to vector
print("1. Converting question to embedding...")
response = ai_client.models.embed_content(
    model='gemini-embedding-2',
    contents=user_question
)
question_vector = response.embeddings[0].values

# 3. Retrieve relevant documents
print("2. Searching database for context...")
results = collection.query(
    query_embeddings=[question_vector],
    n_results=2
)

# Extract the text chunks and combine them into one big string
retrieved_chunks = results['documents'][0]
context_text = "\n".join(retrieved_chunks)
print(f"   Found {len(retrieved_chunks)} relevant chunks.\n")

# 4. Build the Strict RAG Prompt
print("3. Building prompt and sending to LLM...")
prompt = f"""
Answer the user's question using ONLY the context provided below. 
If the context does not contain the exact answer, say "I don't know based on the provided context." Do not guess.

Context:
{context_text}

Question:
{user_question}
"""

# 5. Generate the Final Answer
llm_response = ai_client.models.generate_content(
    model='gemini-3.5-flash',
    contents=prompt
)

print("\n================ FINAL ANSWER ================")
print(llm_response.text)
print("==============================================")
