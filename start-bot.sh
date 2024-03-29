#!/bin/bash

# Absolute path to the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Activate the Python virtual environment
source "${SCRIPT_DIR}/back/pz_python/bin/activate"

# Change working directory
cd "${SCRIPT_DIR}/back/pz_bot" || { echo "The 'back/pz_bot' directory was not found."; exit 1; }

# Start the application
python3 pz_bot.py