#!/bin/bash
# Installer for the Empirical AI Semantic Framework dependencies

echo "Installing dependencies from requirements.txt..."

# Check if pip is available
if ! command -v pip &> /dev/null
then
    echo "Error: pip is not installed. Please install pip to continue." >&2
    exit 1
fi

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Error: Failed to install dependencies. Please check the output above." >&2
    exit 1
fi
