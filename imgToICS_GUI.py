import PySimpleGUI as sg
import os
import base64
import requests
import datetime
from dotenv import load_dotenv


eventTitle = "Event Title Not Initalized"
current_date = datetime.date.today()

load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_ics_file(image_path, api_key, output_dir):
    if not image_path:
        raise ValueError("No image path specified.")
    if not os.path.exists(image_path):
        raise FileNotFoundError("The specified image path does not exist.")
    if not api_key:
        raise ValueError(
            "API key is missing. Make sure to provide a valid API key in the input box.")
    if not output_dir:
        raise RuntimeError("Output directory is not specified.")
    if not os.access(output_dir, os.W_OK):
        raise PermissionError("Output exit_directory is not writable.")

    base64_image = encode_image(image_path)
    promptString = f'Review the image. Take in all information related to the event and Output ONLY the raw text of a .ICS file about the calendar event. Make sure to include Created-By-Ryan-Majd in the PRODID. Also, assume the current year is {current_date.year}.'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

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

    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    ics_content = response.json()['choices'][0]['message']['content']
    begin_index = ics_content.find("BEGIN:VCALENDAR")
    end_index = ics_content.find("END:VCALENDAR") + len("END:VCALENDAR")
    start_index = ics_content.find("SUMMARY:") + len("SUMMARY:")
    end_index = ics_content.find("\n", start_index)
    eventTitle = ics_content[start_index:end_index].strip()
    # Return the stripped content
    ics_content = ics_content[begin_index:end_index]
    # print(ics_content)
    file_path = os.path.join(output_dir, f'{eventTitle}.ics')
    with open(file_path, 'w') as file:
        file.write(ics_content)
        print("Response saved to " + eventTitle + ".ics")
    return ics_content


default_folder = os.path.expanduser("~/Documents/")

# All the stuff inside your window.
layout = [
    [sg.Text("Select Image"), sg.Input(), sg.FileBrowse()],
    [sg.Text("Enter OPENAI API Key"), sg.InputText(
        default_text=KEY if KEY else '')],
    [sg.Text("Select Output Location"), sg.InputText(
        default_text=default_folder), sg.FolderBrowse()],
    [sg.Button('Generate ICS'), sg.Button('Quit')],
    [sg.Text('API Keys are not taken or stored')]
]

# Create the Window
window = sg.Window('Image to ICS', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks quit
    if event == sg.WIN_CLOSED or event == 'Quit':
        break

    if event == 'Generate ICS':
        if values[0] and values[1]:  # Ensure both image path and API key are provided
            if not values[2]:
                sg.popup('Output required')
            output_ics = generate_ics_file(values[0], values[1], values[2])
            sg.popup('ICS file has been saved successfully!')
        else:
            sg.popup('Please provide an image, output, and an API key.')

window.close()
