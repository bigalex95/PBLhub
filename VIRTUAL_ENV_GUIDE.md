# Virtual Environment Setup Guide

This guide covers the mandatory virtual environment setup for the PBLhub Python projects.

## 🚀 Quick Start (Recommended)

### Option 1: Global Virtual Environment

```bash
# Setup everything in one command
python3 tools/setup-venv.py setup-global

# Activate the environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### Option 2: UV Package Manager (Modern Alternative)

```bash
# Setup UV for ultra-fast package management
python3 tools/setup-uv.py setup-all

# Use UV commands
uv sync  # Install all dependencies
uv run --directory projects/01-file-organizer python main.py
```

## 📋 All Available Commands

### Environment Management

```bash
# Check current environment status
python3 tools/env-manager.py status

# Setup recommended environment (global venv + dependencies)
python3 tools/env-manager.py setup

# Show usage examples
python3 tools/env-manager.py examples

# Clean up all environments
python3 tools/env-manager.py cleanup
```

### Virtual Environment Setup

```bash
# Create global virtual environment
python3 tools/setup-venv.py create-global

# Create individual project virtual environments
python3 tools/setup-venv.py create-individual

# Install dependencies in global venv
python3 tools/setup-venv.py install-global

# Install dependencies in individual venvs
python3 tools/setup-venv.py install-individual

# Complete setup (create + install) - Global
python3 tools/setup-venv.py setup-global

# Complete setup (create + install) - Individual
python3 tools/setup-venv.py setup-individual
```

### UV Package Manager (Optional)

```bash
# Install UV (if not already installed)
python3 tools/setup-uv.py install

# Check UV installation
python3 tools/setup-uv.py check

# Setup UV for all projects
python3 tools/setup-uv.py setup-all

# Setup UV for specific project
python3 tools/setup-uv.py setup-project 01-file-organizer

# Sync dependencies
python3 tools/setup-uv.py sync

# Run project with UV
python3 tools/setup-uv.py run 01-file-organizer

# Add package to project
python3 tools/setup-uv.py add requests 04-web-scraper
```

### Wrapper Script (Convenient)

```bash
# Setup global virtual environment
./tools/python.sh setup-venv

# Setup individual virtual environments
./tools/python.sh setup-venv individual

# Setup UV package manager
./tools/python.sh setup-uv

# Install dependencies
./tools/python.sh install

# Run all projects
./tools/python.sh run

# Show activation command
./tools/python.sh activate

# Clean cache files
./tools/python.sh clean

# Remove all virtual environments
./tools/python.sh clean-venv
```

### Dependency Management

```bash
# Install dependencies (uses virtual environment if available)
python3 tools/install-deps.py

# Install to system Python (not recommended)
python3 tools/install-deps.py --no-venv
```

### Project Execution

```bash
# Run all projects
python3 tools/run-all.py

# Verify setup is working
python3 tools/verify-setup.py
```

## 🎯 Recommended Workflows

### For Beginners

1. **Setup**: `python3 tools/env-manager.py setup`
2. **Activate**: `source venv/bin/activate`
3. **Work**: Edit and run projects normally
4. **Deactivate**: `deactivate` when done

### For Modern Python Development

1. **Setup**: `python3 tools/setup-uv.py setup-all`
2. **Work**: `uv run --directory projects/PROJECT_NAME python main.py`
3. **Add packages**: `uv add --directory projects/PROJECT_NAME PACKAGE_NAME`

### For Isolated Development

1. **Setup**: `python3 tools/setup-venv.py setup-individual`
2. **Activate**: `source projects/PROJECT_NAME/venv/bin/activate`
3. **Work**: `cd projects/PROJECT_NAME && python main.py`

## 🔍 Status Checking

Always check your environment status:

```bash
python3 tools/env-manager.py status
```

This shows:

- ✅/❌ Global virtual environment status
- ✅/❌ UV installation and configuration
- ✅/❌ Individual project environment status
- 📊 Summary statistics

## 🛠️ Troubleshooting

### Common Issues

1. **"python: command not found"**

   - Use `python3` instead of `python`
   - The scripts are designed for Python 3.6+

2. **Virtual environment not activating**

   ```bash
   # Check if venv exists
   ls -la venv/

   # Recreate if needed
   python3 tools/setup-venv.py create-global
   ```

3. **Dependencies not installing**

   ```bash
   # Check if you're in virtual environment
   python3 tools/env-manager.py status

   # Install without venv as fallback
   python3 tools/install-deps.py --no-venv
   ```

4. **UV not working**

   ```bash
   # Check UV installation
   python3 tools/setup-uv.py check

   # Reinstall UV
   python3 tools/setup-uv.py install
   ```

### Environment Cleanup

If something goes wrong, you can always start fresh:

```bash
# Clean everything
python3 tools/env-manager.py cleanup

# Or use wrapper
./tools/python.sh clean-venv

# Then setup again
python3 tools/env-manager.py setup
```

## 📁 Environment Structure

After setup, your directory structure will look like:

```
PBLhub/
├── venv/                    # Global virtual environment
├── uv.toml                 # UV workspace configuration (if using UV)
├── projects/
│   ├── 01-file-organizer/
│   │   ├── venv/           # Individual venv (optional)
│   │   ├── pyproject.toml  # UV config (optional)
│   │   ├── requirements.txt
│   │   └── main.py
│   └── ...
└── tools/
    ├── setup-venv.py       # Virtual environment setup
    ├── setup-uv.py         # UV package manager setup
    ├── env-manager.py      # Environment management
    ├── install-deps.py     # Dependency installer
    ├── run-all.py          # Project runner
    ├── python.sh           # Wrapper script
    └── verify-setup.py     # Setup verification
```

## � Version Control & Git

The project's `.gitignore` is configured to handle UV files appropriately:

### What's Tracked:

- ✅ `requirements.txt` files (for compatibility)
- ✅ `uv.toml` workspace configuration (for team setup)
- ✅ Project source code (`main.py`, etc.)

### What's Ignored:

- ❌ `uv.lock` (lockfiles can be environment-specific)
- ❌ `.python-version` files
- ❌ `__pypackages__/` directories
- ❌ `.uv-cache/` directories
- ❌ `projects/*/pyproject.toml` (auto-generated)
- ❌ Virtual environment directories (`venv/`, `.venv/`)

This setup ensures compatibility between `requirements.txt` and UV approaches while keeping the repository clean.

## �💡 Best Practices

1. **Always use virtual environments** - Never install packages globally
2. **Choose one approach** - Either global venv OR individual venvs OR UV
3. **Check status regularly** - Use `env-manager.py status`
4. **Keep dependencies updated** - Regularly update requirements.txt
5. **Use UV for modern projects** - It's faster and more reliable
6. **Activate before coding** - Always activate your virtual environment

## 📚 Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [UV Documentation](https://docs.astral.sh/uv/)
- [PBLhub BUILD_SETUP.md](../BUILD_SETUP.md) - Complete project documentation
