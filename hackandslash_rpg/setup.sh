#!/bin/bash

# Create the virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate it
source .venv/Scripts/activate

# Install/update project dependencies
python -m pip install -r requirements.txt

echo "Environment setup complete."