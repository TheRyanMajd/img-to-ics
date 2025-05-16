import PySimpleGUI as sg
import os
import base64
import requests
import datetime
from dotenv import load_dotenv
from PIL import Image
import pytesseract

eventTitle = "Event Title Not Initalized"
load_dotenv()
KEY = os.getenv('OPENAI_API_KEY')


def ocr_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img, config="--oem 3 --psm 6")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_ics_file(image_path, api_key, output_dir, *, ocr_only=False):
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
    today = datetime.date.today()
    promptString = (
        "Review the event details below and output ONLY the raw text of a .ICS file "
        "for the calendar event. Make sure to include Created-By-Ryan-Majd in the "
        f"PRODID. Assume all dates are in the future. Current date: {today} If end time is NOT provided, assume events will last 3 hours. If there is information not applicable to the iCalendar standard-- drop it in the DESCRIPTION.")
    if ocr_only:
        flyer_text = ocr_image(image_path)
        user_content = [
            {"type": "text",
             "text": promptString + " The following is OCR data extracted with pytesseract:"
             + flyer_text}
        ]
    else:
        base64_image = encode_image(image_path)
        user_content = [
            {"type": "text", "text": promptString},
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": user_content}],
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    ics_content = response.json()['choices'][0]['message']['content']
    begin_index = ics_content.find("BEGIN:VCALENDAR")
    end_index = ics_content.find("END:VCALENDAR") + len("END:VCALENDAR")

    stripped_ics_content = ics_content[begin_index:end_index]

    begin_index = ics_content.find("SUMMARY:") + len("SUMMARY:")
    end_index = ics_content.find("\n", begin_index)
    eventTitle = ics_content[begin_index:end_index].strip()
    # Return the stripped content
    # print(ics_content)
    file_path = os.path.join(output_dir, f'{eventTitle}.ics')
    with open(file_path, 'w') as file:
        file.write(stripped_ics_content)
        print("Response saved to " + eventTitle + ".ics")
    return ics_content


default_folder = os.path.expanduser("~/Documents/")

layout = [
    [sg.Text("Select Image"), sg.Input(key='-IMAGE-'), sg.FileBrowse()],
    [sg.Text("Enter OPENAI API Key"), sg.Input(
        key='-API-KEY-', setting='api_key')],
    [sg.Text("Select Output Location"), sg.InputText(
        key='-OUTPUT-', setting=default_folder), sg.FolderBrowse()],
    [sg.Checkbox("OCR-only (beta, uses local pytesseract)", key='-OCR-')],
    [sg.Button('Generate ICS'), sg.Button('Quit')],
    [sg.Text('API Keys are not taken or stored in the code.')]
]

# Create the Window
window = sg.Window('Image to ICS', layout, enable_close_attempted_event=True,
                   print_event_values=False, auto_save_location=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks quit
    if event == sg.WIN_CLOSED or event == 'Quit':
        window.settings_save(values)
        break

    if event == 'Generate ICS':
        ocr_only = values['-OCR-']
        image_path = values['-IMAGE-']
        api_key = values['-API-KEY-']
        output_path = values['-OUTPUT-']
        if not (image_path and api_key and output_path):
            sg.popup('Please provide an image, API key, and output location.')
        else:
            output_ics = generate_ics_file(image_path, api_key, output_path)
            sg.popup('ICS file has been saved successfully!')

window.close()
