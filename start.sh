#!/bin/bash

# Absolute path to the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Activate the Python virtual environment
source "${SCRIPT_DIR}/back/pz_python/bin/activate"

# Change working directory
cd "${SCRIPT_DIR}/back" || { echo "The 'back' directory was not found."; exit 1; }

# Execute the Python script
python3 main.py
