import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 1. Our helper function to create vectors
def get_embedding(text):
    response = ai_client.models.embed_content(
        model='gemini-embedding-2',
        contents=text
    )
    return response.embeddings[0].values

# 2. Initialize ChromaDB (This creates a folder called 'chroma_db' in your project)
db = chromadb.PersistentClient(path="./chroma_db")

# A 'collection' is like a table in a normal database
collection = db.get_or_create_collection(name="internship_knowledge")

# 3. Our mini "documents"
documents = [
    "The internship duration is exactly 8 weeks.",
    "Students must maintain 75% attendance to pass.",
    "Hostel fees are 5000 rupees per semester."
]

print("Generating embeddings and saving to database...")
embeddings = [get_embedding(doc) for doc in documents]

# 4. Save everything to Chroma
collection.upsert(
    ids=["doc1", "doc2", "doc3"],
    documents=documents,
    embeddings=embeddings
)
print("Documents saved successfully!\n")

# 5. Let's do a search!
user_question = "How long is the internship?"
print(f"User Question: '{user_question}'")

question_vector = get_embedding(user_question)

# Ask Chroma to find the 2 most similar documents using math
results = collection.query(
    query_embeddings=[question_vector],
    n_results=2
)

print("\n--- Top 2 Results from ChromaDB ---")
# results['documents'][0] contains the top matches
for i, doc in enumerate(results['documents'][0]):
    # Chroma returns a "distance" score (lower is closer/better)
    distance = results['distances'][0][i]
    print(f"{i+1}. {doc} (Distance: {distance:.4f})")
