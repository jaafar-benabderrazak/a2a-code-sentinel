#!/bin/bash
# Run script for a2a-mini-1-basic-communication (Linux/macOS)
# Supports both uv and traditional Python

echo "🚀 Running A2A Code Review System..."
echo ""

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "✨ Using uv (fast mode)"
    uv run python main.py
else
    echo "⚙️  Using traditional Python"
    export PYTHONPATH="$PWD"
    python main.py
fi

