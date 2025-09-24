#!/bin/bash

# Python Environment Setup Script
# This script sets up the Python development environment for PBL projects

set -e  # Exit on any error

echo "🐍 Setting up Python development environment..."
echo "=============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $python_version"

# Check if we're in the python branch
if [ ! -f "README.md" ] || ! grep -q "Python Learning Journey" README.md; then
    echo "❌ Error: Make sure you're in the python branch root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install common dependencies
if [ -f "resources/requirements.txt" ]; then
    echo "📦 Installing common dependencies..."
    pip install -r resources/requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  No requirements.txt found, installing basic packages..."
    pip install black flake8 pytest requests beautifulsoup4 pandas
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Virtual Environment
venv/
env/
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
temp/
tmp/
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "🎉 Python environment setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
echo "Happy coding! 🐍✨"
