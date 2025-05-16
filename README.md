# imgToICS — Image-to-Calendar with GPT-4o

by [Ryan Majd](https://ryanmajd.com)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![imgToICSBanner](/banner.svg)

Convert any event flyer (JPEG/PNG) straight into a ready-to-import **.ics** calendar file.

Two Ways to Tango:

- **GUI** (`imgToICS_GUI.py`) – drag-and-drop window with an **“OCR-only (beta)”** checkbox.
- **CLI** (`imgToICS_CLI.py`) – terminal tool; add `-o` or `--ocr-only` to enable the same mode (Does not send image to OpenAI).

![GUI screenshot](/gui_image.svg)

---

## Requirements

| Type                | What you need                                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python**          | 3.8+ (tested on 3.12)                                                                                                                                     |
| **Python packages** | install with `./install_py_pkgs.sh` _or_<br>`pip install PySimpleGUI requests python-dotenv pillow pytesseract`                                           |
| **System package**  | `tesseract-ocr` binary<br>macOS `brew install tesseract` · Ubuntu (usually preinstalled) `sudo apt install tesseract-ocr` · Windows installer.. Google it |
| **OpenAI API key**  | Key with GPT-4o multimodal access (funded ≥ \$5)                                                                                                          |

## Installation

```bash
git clone https://github.com/TheRyanMajd/img-to-ics
cd img-to-ics

# choose ONE of the following
./install_py_pkgs.sh
#   or
pip install PySimpleGUI requests python-dotenv pillow pytesseract
```

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY='sk-xxxxxxxx'
```

---

## Quick Start

### GUI

```bash
python imgToICS_GUI.py
```

1. Select image.
2. Paste your OpenAI key (auto-fills from `.env` if present).
3. Choose output folder.
4. _(Optional)_ Tick **OCR-only (beta)** to keep the flyer image local.
5. Click **Generate ICS** – your calendar file appears in the folder you picked.

### CLI

```bash
python imgToICS_CLI.py <image_path> <output_dir> [-o | --ocr-only]
```

Examples

```bash
# Standard multimodal
python imgToICS_CLI.py flyers/hackathon.png ~/CalendarEvents/

# Offline OCR only
python imgToICS_CLI.py flyers/hackathon.png ~/CalendarEvents/ --ocr-only
```

---

## How It Works

1. **Image mode** – base-64 image → OpenAI Vision → iCalendar text.
2. **OCR-only** – local Tesseract → raw text → GPT-4o (text only).
3. Script extracts everything from `BEGIN:VCALENDAR` to `END:VCALENDAR`, names the file from the `SUMMARY`, and writes it.

Default assumptions:

- All dates are treated as _future_ dates... _cause why the hell would you want to book events back in time_
- If no end time is provided, the event is set to **3 hours**.
  - Maybe I'll add a defaults.json file so that y'all can change these easier...

---

## Key Libraries

- **PySimpleGUI** – cross-platform UI
- **Pillow** (`PIL`) – image handling
- **pytesseract** – OCR
- **requests** – HTTPS calls
- **python-dotenv** – keeps secrets out of source

---

## Security & Privacy

- API keys stay in memory only – never written to disk or sent anywhere else.
- In OCR-only mode the image never leaves your computer.
- Always glance over the generated `.ics` before sharing since AI hallucinates a lot.

---

## Roadmap

- [x] OCR fallback
- [x] Date disambiguation improvements
- [ ] Batch-process entire folders of images
- [ ] Unit tests & CI
- [ ] Whatever cool idea y'all suggest

---

## License

MIT — see `LICENSE`.
