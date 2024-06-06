import os
import sys
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

args = sys.argv
if len(args) != 3:
    print("Usage: imgToICS_CLI.py input_file output_location")
    sys.exit(1)
input_file = args[1]
output_dir = args[2]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


verbose = False  # change to true if you want to print the output of the .ics file
image_path = input_file
base64_image = encode_image(image_path)
promptString = 'Review the image. Take in all information related to the event and Output ONLY the raw text of a .ICS file about the calendar event. Make sure to include Created-By-Ryan-Majd in the PRODID. Also, the year is 2024.'
load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')

if not image_path:
    raise ValueError("No image path specified.")
if not os.path.exists(image_path):
    raise FileNotFoundError("The specified image path does not exist.")
if not KEY:
    raise ValueError(
        "API key and/or .env file is missing. Make sure to provide a valid API key in this format: OPENAI_API_KEY = 'APIKEYHERE'")
if not output_dir:
    raise RuntimeError("Output directory is not specified.")
if not os.access(output_dir, os.W_OK):
    raise PermissionError("Output exit_directory is not writable.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KEY}"
}
# Load the environment variables
payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": promptString
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
ics_content = response.json()['choices'][0]['message']['content']
begin_index = ics_content.find("BEGIN:VCALENDAR")
end_index = ics_content.find("END:VCALENDAR") + len("END:VCALENDAR")
# Print the stripped content
stripped_ics_content = ics_content[begin_index:end_index]

begin_index = ics_content.find("SUMMARY:") + len("SUMMARY:")
end_index = ics_content.find("\n", begin_index)
eventTitle = ics_content[begin_index:end_index].strip()
if verbose:
    print(stripped_ics_content)

file_path = os.path.join(output_dir, f'{eventTitle}.ics')
with open(file_path, 'w') as file:
    file.write(stripped_ics_content)
print(f"✅ Response saved to {file_path}")
