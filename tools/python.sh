#!/bin/bash

# Python Project Runner
# Wrapper script for easier execution

echo "🐍 Python Project Management"
echo "============================="

case "$1" in
    "run")
        echo "Running all Python projects..."
        python3 tools/run-all.py
        ;;
    "install")
        echo "Installing dependencies for all projects..."
        python3 tools/install-deps.py
        ;;
    "clean")
        echo "Cleaning Python cache files..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        echo "✅ Python cache cleaned"
        ;;
    *)
        echo "Usage: $0 {run|install|clean}"
        echo ""
        echo "Commands:"
        echo "  run     - Run all Python projects"
        echo "  install - Install all dependencies"
        echo "  clean   - Clean Python cache files"
        echo ""
        echo "Examples:"
        echo "  ./tools/python.sh run"
        echo "  ./tools/python.sh install"
        echo "  python3 projects/01-file-organizer/main.py"
        exit 1
        ;;
esac