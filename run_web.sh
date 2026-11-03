#!/usr/bin/env bash
# run_web.sh - Starts the Kaedehara Kazuha SQL Sanctuary Web Server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/python" ]; then
    echo "🍁 Starting Kaedehara Kazuha SQL Sanctuary via virtualenv..."
    .venv/bin/python app.py
else
    echo "🍁 Starting Kaedehara Kazuha SQL Sanctuary via python3..."
    python3 app.py
fi
