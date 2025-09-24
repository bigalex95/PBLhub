#!/usr/bin/env python3
"""
Install Dependencies Script
This script installs all dependencies for Python projects
Supports virtual environments and UV package manager
"""

import subprocess
import sys
import os
from pathlib import Path


# Import centralized project configuration
def get_projects_config():
    """Get project configuration with proper error handling"""
    try:
        # Try relative import first
        from .project_config import get_project_names, ProjectConfig

        return get_project_names, ProjectConfig
    except ImportError:
        # Handle direct execution
        import importlib.util

        config_path = Path(__file__).parent / "project_config.py"
        if config_path.exists():
            spec = importlib.util.spec_from_file_location("project_config", config_path)
            if spec and spec.loader:
                project_config = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(project_config)
                return project_config.get_project_names, project_config.ProjectConfig

    # Fallback to hardcoded list if project_config is not available
    def fallback_get_project_names():
        return [
            "01-file-organizer",
            "02-password-generator",
            "03-expense-tracker",
            "04-web-scraper",
            "05-api-client",
            "06-task-scheduler",
            "07-data-analyzer",
            "08-mini-framework",
        ]

    class FallbackProjectConfig:
        def get_project_names(self):
            return fallback_get_project_names()

    return fallback_get_project_names, FallbackProjectConfig


def get_pip_command(project_path=None, use_venv=True):
    """Get the appropriate pip command based on environment"""
    if not use_venv:
        return [sys.executable, "-m", "pip"]

    # Check for global venv first
    global_venv = Path("venv")
    if global_venv.exists() and not project_path:
        if os.name == "nt":  # Windows
            return [str(global_venv / "Scripts" / "python"), "-m", "pip"]
        else:  # Unix-like
            return [str(global_venv / "bin" / "python"), "-m", "pip"]

    # Check for project-specific venv
    if project_path:
        project_venv = project_path / "venv"
        if project_venv.exists():
            if os.name == "nt":  # Windows
                return [str(project_venv / "Scripts" / "python"), "-m", "pip"]
            else:  # Unix-like
                return [str(project_venv / "bin" / "python"), "-m", "pip"]

    # Fall back to system Python
    return [sys.executable, "-m", "pip"]


def install_requirements(project_path, use_venv=True):
    """Install requirements for a single project"""
    requirements_file = project_path / "requirements.txt"

    if not requirements_file.exists():
        return True, "No requirements.txt found"

    # Check if requirements file is just a comment (no real dependencies)
    content = requirements_file.read_text().strip()
    if not content or content.startswith("#"):
        return True, "No dependencies needed"

    try:
        pip_cmd = get_pip_command(project_path, use_venv)
        cmd = pip_cmd + ["install", "-r", str(requirements_file)]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            venv_info = " (in venv)" if use_venv else " (system)"
            return True, f"Dependencies installed successfully{venv_info}"
        else:
            return False, result.stderr.strip() or "Unknown error"

    except Exception as e:
        return False, str(e)


def main():
    print("📦 Installing dependencies for all Python projects...")
    print("=" * 60)

    # Parse command line arguments
    use_venv = "--no-venv" not in sys.argv

    # Check environment setup
    global_venv = Path("venv")
    if use_venv and global_venv.exists():
        print("🐍 Using global virtual environment at ./venv")
    elif use_venv:
        print("⚠️  No global virtual environment found.")
        print("💡 Run 'python tools/setup-venv.py setup-global' to create one")
        print("   Or use '--no-venv' flag to install to system Python")

    # Check if we're in the python branch
    projects_dir = Path("projects")
    if not projects_dir.exists():
        print(
            "❌ Error: projects/ directory not found. Make sure you're in the python branch root."
        )
        sys.exit(1)

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    if not projects:
        print("❌ No projects found!")
        sys.exit(1)

    successful_installs = []
    failed_installs = []
    skipped_projects = []

    print("📥 Installing dependencies for each project...")
    print()

    # Install dependencies for each project
    for project_name in projects:
        project_path = projects_dir / project_name

        if not project_path.exists():
            print(f"⚠️  Project directory {project_name} not found, skipping...")
            continue

        print(f"📦 Installing dependencies for {project_name}...")

        success, message = install_requirements(project_path, use_venv)

        if success:
            if "No dependencies" in message or "No requirements" in message:
                print(f"ℹ️  {project_name}: {message}")
                skipped_projects.append(project_name)
            else:
                print(f"✅ {project_name}: {message}")
                successful_installs.append(project_name)
        else:
            print(f"❌ {project_name} failed: {message}")
            failed_installs.append((project_name, message))

        print()

    # Summary
    print("📊 Installation Summary")
    print("=" * 30)
    print(f"Total projects: {len(projects)}")
    print(f"✅ Successfully installed: {len(successful_installs)}")
    print(f"ℹ️  No dependencies needed: {len(skipped_projects)}")
    print(f"❌ Failed installations: {len(failed_installs)}")
    print()

    if successful_installs:
        print("🎉 Dependencies installed for:")
        for project in successful_installs:
            print(f"  ✅ {project}")
        print()

    if skipped_projects:
        print("ℹ️  No external dependencies needed for:")
        for project in skipped_projects:
            print(f"  📝 {project}")
        print()

    if failed_installs:
        print("⚠️  Failed to install dependencies for:")
        for project, error in failed_installs:
            print(f"  ❌ {project}: {error}")
        print()
        print("🛠️  Fix the errors and run ./tools/install-deps.py again")
        print()
        print("💡 Common solutions:")
        print("  - Make sure pip is installed: python -m ensurepip")
        print("  - Upgrade pip: python -m pip install --upgrade pip")
        print("  - Setup virtual environment: python tools/setup-venv.py setup-global")
        print("  - Use system Python: python tools/install-deps.py --no-venv")
        print("  - Check internet connection")
        sys.exit(1)
    else:
        print("🎉 All dependencies installed successfully!")
        print("💡 Next steps:")
        if use_venv and global_venv.exists():
            print("  source venv/bin/activate  # Activate global venv (Linux/Mac)")
            print("  # OR venv\\Scripts\\activate  # Activate global venv (Windows)")
        print("  ./tools/run-all.py  # Run all projects")
        print("  python projects/PROJECT_NAME/main.py  # Run individual project")
        sys.exit(0)


if __name__ == "__main__":
    main()
