#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "Activity Monitor installer — setting up virtual environment and dependencies"

PY=python3
PIP=pip3

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "Error: $PY not found. Please install Python 3."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv..."
  "$PY" -m venv .venv
fi

echo "Activating virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip >/dev/null

if [ -f requirements.txt ]; then
  echo "Installing from requirements.txt..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found — installing default packages..."
  pip install psutil matplotlib fpdf
fi

echo "Installation finished."
echo "To run the app:"
echo "  source .venv/bin/activate"
echo "  python3 main.py"

if [ "${1:-}" = "--run" ]; then
  echo "Starting Activity Monitor... (press Ctrl-C to stop)"
  python3 main.py
fi

exit 0
