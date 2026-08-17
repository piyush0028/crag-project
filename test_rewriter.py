import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def rewrite_query(original_question):
    prompt = f"""
    You are an expert at searching databases. The user's original search query failed
    to find good results. 
    
    Rewrite the query to be more descriptive and use synonyms that might be found
    in official documentation. Keep it to one single sentence.
    
    Original Query: {original_question}
    
    Rewritten Query:
    """
    
    response = ai_client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    # .strip() removes any accidental spaces or newlines at the start/end
    return response.text.strip()

print("Testing Query Rewriting...\n")

# Example 1: Vague keyword search
q1 = "internship rules"
print(f"Original: '{q1}'")
print(f"Rewritten: '{rewrite_query(q1)}'\n")

# Example 2: Conversational slang
q2 = "how much do I gotta pay for the dorms?"
print(f"Original: '{q2}'")
print(f"Rewritten: '{rewrite_query(q2)}'\n")
