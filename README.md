# imgToICS using GPT4o

##### by [Ryan Majd](mailto:ryan.majd@uga.edu)

![imgToICSBanner](/banner.svg)

## Overview

The `imgToICS` application is designed to convert images/flyers containing event details into ICS (iCalendar) files. It is programmed in Python and available in two formats: a graphical user interface (GUI) and a command line interface (CLI).
![imgToICSBanner](/gui_image.svg)

This is my first python application that I am releasing to the public, so please go easy on me 😸!

## Requirements

- Python 3.6 or higher
- Python libraries installable using `install_py_pkgs.sh`
- Internet connection for API requests
- [OpenAI API Key](https://platform.openai.com/api-keys)

## Libraries

- `PySimpleGUI` for `imgToICS_GUI.py` file only
- `os` for outputting the ics file
- `requests` for HTTP requests
- `datetime` for handling dates
- `dotenv` for loading environment variables (`.env`)

## Setup

1. Install the required Python packages:
   ```bash
   pip install PySimpleGUI requests python-dotenv
   ```
2. Ensure you have an API key from OpenAI for GPT-4 model access and you provided a minimum of $5 to utilize their multimodal LLMS (such as gpt-4o).
3. **CLI USERS ONLY:** Create a `.env` file in the application directory and store your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY='apikey'
   ```

## Using imgToICS_GUI.py

The GUI version provides a user-friendly interface for generating ICS files:

- Run the script:
  ```bash
  python3 imgToICS_GUI.py
  ```
- Fill in the fields for the image path, API key, and output directory (some may be preloaded).
- Click 'Generate ICS' to process the image and generate the ICS file!

## Using imgToICS_CLI.py

The CLI version is streamlined for command line usage:

- Usage:
  ```bash
  python3 imgToICS_CLI.py <input_file> <output_location>
  ```
- Provide the path to the image file and the desired output directory as command line arguments.

## File Generation

Both versions of the application will:

- Encode the provided image to base64.
- Send a request to OpenAI's API using the encoded image.
- Parse the response to create an ICS file containing the event details.
- Save the ICS file in the specified output directory.

## Security Notes

- API keys are not stored or logged by the application through the code, ensuring your credentials remain secure. (Now utilizing PySimpleGUI 5's parameter element)
- Always verify outputs for accuracy and completeness.
- This project is open-sourced 😺
