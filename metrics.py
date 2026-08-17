import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def evaluate_faithfulness(question, context, answer):
    prompt = f"""
    You are a strict grader. 
    Given the Question, Context, and Final Answer, determine if the Final Answer 
    is ENTIRELY supported by the Context. 
    If the answer includes made-up facts not found in the context, output exactly 0.
    If the answer is completely supported by the context, output exactly 1.
    
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Output only a 1 or a 0.
    """
    response = ai_client.models.generate_content(
        model='gemini-3.6-flash', contents=prompt
    )
    return int(response.text.strip())

def evaluate_answer_relevance(question, answer):
    prompt = f"""
    You are a strict grader.
    Does this Answer directly address the user's Question?
    Output exactly 1 if yes, or exactly 0 if it is evasive or off-topic.
    
    Question: {question}
    Answer: {answer}
    
    Output only a 1 or a 0.
    """
    response = ai_client.models.generate_content(
        model='gemini-3.6-flash', contents=prompt
    )
    return int(response.text.strip())

# Let's test our evaluator!
print("Running Automated Evaluation...\n")

test_q = "How long is the internship?"
test_c = "The internship duration is exactly 8 weeks."

# Scenario A: A perfect answer
good_answer = "The internship lasts for 8 weeks."
print("Testing Good Answer:")
print(f"Faithfulness Score: {evaluate_faithfulness(test_q, test_c, good_answer)}")
print(f"Relevance Score: {evaluate_answer_relevance(test_q, good_answer)}\n")

# Scenario B: A hallucinated answer (LLM made up facts)
bad_answer = "The internship lasts for 8 weeks and you get paid $5000."
print("Testing Hallucinated Answer:")
print(f"Faithfulness Score: {evaluate_faithfulness(test_q, test_c, bad_answer)}")
print(f"Relevance Score: {evaluate_answer_relevance(test_q, bad_answer)}")
