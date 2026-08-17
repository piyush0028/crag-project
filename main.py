import os
import chromadb
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_collection(name="internship_knowledge")

# --- Helper Functions (From your CRAG Pipeline) ---
def get_embedding(text):
    return ai_client.models.embed_content(model='gemini-embedding-2', contents=text).embeddings[0].values

def retrieve(question):
    vector = get_embedding(question)
    results = collection.query(query_embeddings=[vector], n_results=2)
    return "\n".join(results['documents'][0])

def evaluate(question, context):
    prompt = f"Does this context contain the answer to the question? Reply only YES or NO.\nQuestion: {question}\nContext: {context}"
    response = ai_client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt)
    return response.text.strip().upper()

def rewrite(question):
    prompt = f"Rewrite this search query to be highly professional and use synonyms. Original: {question}"
    response = ai_client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt)
    return response.text.strip()

def generate_answer(question, context):
    prompt = f"Answer using ONLY this context:\n{context}\n\nQuestion: {question}"
    response = ai_client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt)
    return response.text.strip()

# --- FastAPI Setup ---
app = FastAPI()

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data structure for incoming requests
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    user_question = request.question
    agent_logs = [] # Keep track of what the agent is doing to display in the UI
    
    agent_logs.append("Searching database...")
    context = retrieve(user_question)
    
    agent_logs.append("Evaluating retrieved documents...")
    is_good = evaluate(user_question, context)
    
    if "NO" in is_good:
        agent_logs.append("Documents were bad. Rewriting query...")
        better_query = rewrite(user_question)
        agent_logs.append(f"New query -> '{better_query}'")
        agent_logs.append("Searching again with new query...")
        context = retrieve(better_query)
    else:
        agent_logs.append("Documents were good. Proceeding to answer.")
        
    agent_logs.append("Generating final answer...")
    answer = generate_answer(user_question, context)
    
    # Return both the answer and the thought process
    return {"answer": answer, "logs": agent_logs}
