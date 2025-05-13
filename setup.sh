#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
REQ_FILE="requirements.txt"

echo "=== 🔧 Bootstrapping development environment ==="

# 1. Create virtualenv if it doesn't exist
if [ -d "$VENV_DIR" ]; then
  echo "✔️  Virtualenv already exists at $VENV_DIR"
else
  echo "🛠️  Creating virtualenv in $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# 2. Activate it for this script
#    (Note: to persist activation, run `source $VENV_DIR/bin/activate` yourself afterwards)
source "$VENV_DIR/bin/activate"

# 3. Upgrade pip
echo "⬆️  Upgrading pip"
pip install --upgrade pip

# 4. Install runtime dependencies
if [ -f "$REQ_FILE" ]; then
  echo "📦 Installing runtime dependencies from $REQ_FILE"
  pip install -r "$REQ_FILE"
else
  echo "⚠️  No $REQ_FILE found—skipping dependency install"
fi

echo
echo "✅ Setup complete!"
echo "👉 To start working: run 

source $VENV_DIR/bin/activate"
