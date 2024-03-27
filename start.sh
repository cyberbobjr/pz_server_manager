#!/bin/bash

# Absolute path to the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Check if pidfile exists and stop the previous process
if [ -f "${SCRIPT_DIR}/back/pidfile" ]; then
    PID=$(cat "${SCRIPT_DIR}/back/pidfile")
    kill "$PID"
    rm "${SCRIPT_DIR}/back/pidfile"
fi

# Activate the Python virtual environment
source "${SCRIPT_DIR}/back/pz_python/bin/activate"

# Change working directory
cd "${SCRIPT_DIR}/back" || { echo "The 'back' directory was not found."; exit 1; }

# Start the application
uvicorn main:app --host 0.0.0.0 --port 7777 & echo $! > "${SCRIPT_DIR}/back/pidfile"
