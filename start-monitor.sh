#!/bin/bash

# Absolute path to the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Check if pidfile exists
if [ -f "${SCRIPT_DIR}/back/pidfile_monitor" ]; then
    PID=$(cat "${SCRIPT_DIR}/back/pidfile_monitor")
    # Check if the process is running by sending a signal 0
    # If the process exists, kill will succeed, otherwise it will fail
    if kill -0 "$PID" 2>/dev/null; then
        # If the process exists, kill it
        kill "$PID"
    else
        echo "Process with PID $PID not found."
    fi
    # Remove the pidfile
    rm "${SCRIPT_DIR}/back/pidfile_monitor"
fi

# Activate the Python virtual environment
source "${SCRIPT_DIR}/back/pz_python/bin/activate"
echo "Launched in ${SCRIPT_DIR}"

# Change working directory
cd "${SCRIPT_DIR}/back" || { echo "The 'back' directory was not found."; exit 1; }

LOGFILE="${SCRIPT_DIR}/back/logs/pz_monitor.log"
mkdir -p "${SCRIPT_DIR}/back/logs"

# Start the application
python3 pz_monitor/pz_monitor.py >> "$LOGFILE" 2>&1 & echo $! > "${SCRIPT_DIR}/back/pidfile_monitor"
