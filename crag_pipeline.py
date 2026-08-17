import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_collection(name="internship_knowledge")

# --- Helper Functions (The Bricks) ---

def get_embedding(text):
    return ai_client.models.embed_content(
        model='gemini-embedding-2', contents=text
    ).embeddings[0].values

def retrieve(question):
    vector = get_embedding(question)
    results = collection.query(query_embeddings=[vector], n_results=2)
    return "\n".join(results['documents'][0])

def evaluate(question, context):
    prompt = f"""
    Does this context contain the answer to the question? 
    Reply only YES or NO.
    Question: {question}
    Context: {context}
    """
    response = ai_client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text.strip().upper()

def rewrite(question):
    prompt = f"Rewrite this search query to be highly professional and use synonyms. Original: {question}"
    response = ai_client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text.strip()

def generate_answer(question, context):
    prompt = f"Answer using ONLY this context:\n{context}\n\nQuestion: {question}"
    response = ai_client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text.strip()

# --- The Agentic Loop (The Brain) ---

def run_crag(user_question):
    print(f"\nUser asked: '{user_question}'")
    print("-" * 40)
    
    # 1. Initial Retrieval
    print("Agent: Searching database...")
    context = retrieve(user_question)
    
    # 2. Evaluate
    print("Agent: Evaluating retrieved documents...")
    is_good = evaluate(user_question, context)
    print(f"Agent: Evaluator said {is_good}")
    
    # 3. Corrective Action (The Loop)
    if "NO" in is_good:
        print("Agent: Documents were bad. Rewriting query...")
        better_query = rewrite(user_question)
        print(f"Agent: New query -> '{better_query}'")
        
        print("Agent: Searching again with new query...")
        context = retrieve(better_query)
    else:
        print("Agent: Documents were good. Proceeding to answer.")

    # 4. Generate Final Answer
    print("Agent: Generating final answer...")
    answer = generate_answer(user_question, context)
    
    print("\n================ FINAL ANSWER ================")
    print(answer)
    print("==============================================")

# Let's test it with a tricky question!
# "accommodation" might fail initially because our DB uses the word "hostel"
run_crag("How much does accommodation cost?")
