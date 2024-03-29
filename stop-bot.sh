#!/bin/bash

# Absolute path to the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Path to the pid file
PIDFILE="${SCRIPT_DIR}/back/pidfile_bot"

# Check if the pidfile exists
if [ ! -f "$PIDFILE" ]; then
    echo "Le fichier PID n'existe pas : $PIDFILE"
    exit 1
fi

# Read the PID from the pidfile
PID=$(cat "$PIDFILE")

# Check if the process is running
if ps -p "$PID" > /dev/null 2>&1; then
    echo "Arrêt du processus $PID..."
    # Kill the process
    kill "$PID"

    # Wait for the process to terminate
    wait "$PID" 2>/dev/null

    # Remove the pidfile
    rm -f "$PIDFILE"

    echo "Processus arrêté."
else
    echo "Le processus $PID n'est pas en cours d'exécution."
    # Remove
