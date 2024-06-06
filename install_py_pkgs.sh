#!/bin/bash

# Function to check if a Python package is installed
function check_package {
    pip freeze | grep $1 > /dev/null
    if [ $? -eq 0 ]; then
        echo "$1 is already installed."
    else
        echo "$1 is not installed. Installing now..."
        pip install $1
    fi
}

# Check and install packages
check_package PySimpleGUI
check_package requests
check_package python-dotenv
check_package openai

# base64, os, and datetime are part of the Python standard library and do not need to be installed.
echo "base64, os, and datetime are standard library packages and do not require installation."

echo "All packages are checked and installed."
