import os
from dotenv import load_dotenv
from google import genai

# 1. Load the secret variables from the .env file
load_dotenv()

# 2. Initialize the client using your API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("Sending request to the LLM...")

# 3. Make the API call
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Explain what an API is in one short sentence.'
)

# 4. Print the result
print("\n--- Response ---")
print(response.text)