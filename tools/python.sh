#!/bin/bash

# Python Project Runner
# Wrapper script for easier execution with virtual environment support

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
    "setup-venv")
        echo "Setting up virtual environments..."
        if [ "$2" = "individual" ]; then
            python3 tools/setup-venv.py setup-individual
        else
            python3 tools/setup-venv.py setup-global
        fi
        ;;
    "setup-uv")
        echo "Setting up UV package manager..."
        python3 tools/setup-uv.py setup-all
        ;;
    "activate")
        if [ -d "venv" ]; then
            echo "🐍 Activating global virtual environment..."
            echo "Run: source venv/bin/activate"
        else
            echo "❌ No global virtual environment found."
            echo "💡 Run: ./tools/python.sh setup-venv"
        fi
        ;;
    "clean")
        echo "Cleaning Python cache files..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        echo "✅ Python cache cleaned"
        ;;
    "clean-venv")
        echo "Cleaning virtual environments..."
        if [ -d "venv" ]; then
            rm -rf venv/
            echo "✅ Global virtual environment removed"
        fi
        find projects/ -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true
        echo "✅ All project virtual environments removed"
        ;;
    "projects")
        echo "Managing projects..."
        if [ "$2" = "list" ]; then
            python3 tools/project_cli.py list
        elif [ "$2" = "add" ] && [ -n "$3" ]; then
            python3 tools/project_cli.py add "$3"
        elif [ "$2" = "info" ] && [ -n "$3" ]; then
            python3 tools/project_cli.py info "$3"
        else
            echo "Project management commands:"
            echo "  ./tools/python.sh projects list              # List all projects"
            echo "  ./tools/python.sh projects add <name>       # Add new project"
            echo "  ./tools/python.sh projects info <name>      # Show project info"
        fi
        ;;
    "status")
        echo "Checking environment status..."
        python3 tools/env-manager.py status
        ;;
    *)
        echo "Usage: $0 {run|install|setup-venv|setup-uv|activate|clean|clean-venv|projects|status}"
        echo ""
        echo "Commands:"
        echo "  run         - Run all Python projects"
        echo "  install     - Install all dependencies"
        echo "  setup-venv  - Setup virtual environments (global or individual)"
        echo "  setup-uv    - Setup UV package manager for all projects"
        echo "  activate    - Show how to activate global virtual environment"
        echo "  clean       - Clean Python cache files"
        echo "  clean-venv  - Remove all virtual environments"
        echo "  projects    - Manage projects (list, add, info)"
        echo "  status      - Check environment status"
        echo ""
        echo "Examples:"
        echo "  ./tools/python.sh setup-venv          # Setup global venv"
        echo "  ./tools/python.sh setup-venv individual # Setup individual venvs"
        echo "  ./tools/python.sh setup-uv            # Setup UV for all projects"
        echo "  ./tools/python.sh install             # Install dependencies"
        echo "  ./tools/python.sh run                 # Run all projects"
        echo ""
        echo "Virtual Environment Usage:"
        echo "  source venv/bin/activate              # Activate global venv"
        echo "  source projects/PROJECT/venv/bin/activate # Activate project venv"
        exit 1
        ;;
esac