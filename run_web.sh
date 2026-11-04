#!/usr/bin/env bash
# run_web.sh - Starts the Kaedehara Kazuha SQL Sanctuary Web Server on port 12000
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/python" ]; then
    echo "🍁 Starting Kaedehara Kazuha SQL Sanctuary via virtualenv..."
    PYTHON=".venv/bin/python"
else
    echo "🍁 Starting Kaedehara Kazuha SQL Sanctuary via python3..."
    PYTHON="python3"
fi

if ! "$PYTHON" -c "import flask" >/dev/null 2>&1; then
    echo "Flask is not installed. Install the dependencies with:" >&2
    echo "  $PYTHON -m pip install -r requirements.txt" >&2
    exit 1
fi

"$PYTHON" app.py
