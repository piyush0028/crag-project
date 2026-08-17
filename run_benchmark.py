import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def evaluate_faithfulness(question, context, answer):
    prompt = f"""
    You are a strict grader. Output exactly 1 if the Answer is supported by the Context, or 0 if it contains made up facts.
    
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Output only 1 or 0.
    """
    response = ai_client.models.generate_content(
        model='gemini-3.6-flash', contents=prompt
    )
    return int(response.text.strip())

# Our mini Evaluation Dataset
# In a real project, this would be loaded from a CSV or JSON file
dataset = [
    {
        "question": "How long is the internship?",
        "context": "The internship duration is exactly 8 weeks.",
        "system_answer": "It lasts for 8 weeks." # Perfect answer
    },
    {
        "question": "What is the minimum attendance?",
        "context": "Students must maintain 75% attendance to pass.",
        "system_answer": "You need 75% attendance." # Perfect answer
    },
    {
        "question": "What are the hostel fees?",
        "context": "Hostel fees are 5000 rupees per semester.",
        "system_answer": "Fees are 5000 rupees, and meals are included." # Hallucination (meals aren't mentioned!)
    }
]

print("Running Automated Benchmark over 3 test cases...\n")

total_score = 0

for i, item in enumerate(dataset):
    print(f"Evaluating Question {i+1}: '{item['question']}'")
    score = evaluate_faithfulness(item['question'], item['context'], item['system_answer'])
    print(f"  -> Faithfulness Score: {score}")
    total_score += score

# Calculate the final percentage
average = (total_score / len(dataset)) * 100

print("\n================ SYSTEM METRICS ================")
print(f"Overall Faithfulness: {average:.1f}%")
print("================================================")
