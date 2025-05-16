import os
import sys
import base64
import requests
import datetime
from dotenv import load_dotenv
from PIL import Image
import pytesseract

args = sys.argv[1:]
ocr_only = False
if len(args) not in (2, 3):
    print(
        "Usage: imgToICS_CLI.py <input_image> <output_dir> [-o | --ocr-only]")
    sys.exit(1)
if len(args) == 3:
    flag = args.pop()                             # remove the third token
    if flag in ("-o", "--ocr-only"):
        ocr_only = True
        print("⚠️ Warning OCR Mode is in Beta and Relies on pytesseract, "
              "which may not be 100% accurate. Use at your own risk. Always double check output files.")
    else:
        print(f"Unknown option: {flag}")
        sys.exit(1)

input_file, output_dir = args
today = datetime.date.today()


def encode_image(path: str) -> str:
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def ocr_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img, config="--oem 3 --psm 6")


if not os.path.isfile(input_file):
    raise FileNotFoundError(f"Image not found: {input_file}")
if not (os.path.isdir(output_dir) and os.access(output_dir, os.W_OK)):
    raise PermissionError(
        f"Output directory invalid / unwritable: {output_dir}")

load_dotenv()
KEY = os.getenv("OPENAI_API_KEY") or ""
if not KEY:
    raise ValueError("OPENAI_API_KEY missing or empty in .env")

prompt = (
    "Review the event details below and output ONLY the raw text of a .ICS file "
    "for the calendar event. Make sure to include Created-By-Ryan-Majd in the "
    f"PRODID. Assume all dates are in the future. Current date: {today} If end time is NOT provided, assume events will last 3 hours. If there is information not applicable to the iCalendar standard-- throw it in the description."
)

if ocr_only:
    flyer_text = ocr_image(input_file)
    prompt += f"The following is OCR Data from the image/flyer provided using pytesseract this is all you get to go off of: {flyer_text}"
    user_content = [{"type": "text", "text": prompt}]
else:
    base64_img = encode_image(input_file)
    user_content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {
            "url": f"data:image/jpeg;base64,{base64_img}"}}
    ]

payload = {
    "model": "gpt-4o",
    "max_tokens": 300,
    "messages": [{"role": "user", "content": user_content}],
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KEY}",
}

# ──────────────────────────── OPENAI CALL ────────────────────────────
resp = requests.post("https://api.openai.com/v1/chat/completions",
                     headers=headers, json=payload)
resp.raise_for_status()
ics_text = resp.json()["choices"][0]["message"]["content"]

# ──────────────────────────── FILE OUTPUT ────────────────────────────
begin, end = ics_text.find("BEGIN:VCALENDAR"), ics_text.find(
    "END:VCALENDAR")+len("END:VCALENDAR")
ics_body = ics_text[begin:end]

sum_start = ics_body.find("SUMMARY:") + len("SUMMARY:")
sum_end = ics_body.find("\n", sum_start)
event_title = ics_body[sum_start:sum_end].strip() or "event"

out_path = os.path.join(output_dir, f"{event_title}.ics")
with open(out_path, "w") as f:
    f.write(ics_body)

print(f"✅  Saved to {out_path} ({'OCR mode' if ocr_only else 'image mode'})")
