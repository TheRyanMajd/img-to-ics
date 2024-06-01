import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Retrieve the API key correctly
KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key was loaded correctly
if not KEY:
    raise ValueError(
        "API key not found. Check your .env file and ensure it contains 'OPENAI_API_KEY'.")
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get(KEY),
)
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "output ONLY the raw text of a .ICS file about a temporary calendar event",
        }
    ],
    model="gpt-3.5-turbo",
)

print(response.choices[0].message.content)
# # Initialize the OpenAI API with the API key
# openai.api_key = KEY

# # Create a chat completion using the new API method
# response = openai.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": 'output only the raw text of a .ICS file about a temporary calendar event'}
#               ])


# # Save the completion to a file
with open('output.ics', 'w') as file:
    if response.choices[0].message.content:
        file.write(response.choices[0].message.content)
print("Response saved to output.txt")
