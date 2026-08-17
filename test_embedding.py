import os
from dotenv import load_dotenv
from google import genai

# Load your API key
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

text_to_embed = "What is the internship duration?"

print(f"Generating embedding for: '{text_to_embed}'...\n")

# Call the embedding model
response = client.models.embed_content(
    model='gemini-embedding-2',
    contents=text_to_embed
)

# Extract the list of numbers (the vector)
vector = response.embeddings[0].values

print(f"Success! The text was converted into a list of {len(vector)} numbers.")
print(f"Here is a peek at the first 5 numbers:")
print(vector[:5])
