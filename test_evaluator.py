import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def evaluate_retrieval(question, context):
    # We give the LLM a very strict persona and instruction
    prompt = f"""
    You are an expert grading system. Your job is to check if the provided context
    contains enough information to answer the question.
    
    Question: {question}
    
    Context: 
    {context}
    
    Respond with exactly one word: YES if the context is relevant and contains the answer, or NO if it does not.
    """
    
    response = ai_client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    # .strip().upper() ensures the response is clean, e.g., "YES" not " yes "
    return response.text.strip().upper()

print("Testing the CRAG Evaluator...\n")

# Scenario 1: The database returned the correct information
q1 = "What is the internship duration?"
c1 = "The internship duration is exactly 8 weeks."

print("Scenario 1 (Relevant Context):")
print("Result:", evaluate_retrieval(q1, c1))
print("-" * 30)

# Scenario 2: The database returned irrelevant information
q2 = "What is the refund policy?"
c2 = "The internship duration is exactly 8 weeks. Hostel fees are 5000 rupees."

print("Scenario 2 (Irrelevant Context):")
print("Result:", evaluate_retrieval(q2, c2))
