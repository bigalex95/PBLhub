#!/usr/bin/env python3
"""
Virtual Environment Setup Script
This script creates and manages virtual environments for Python projects
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


def run_command(cmd, cwd=None):
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(
            f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.6+"
        )
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_global_venv():
    """Create a global virtual environment for the entire project"""
    venv_path = Path("venv")

    if venv_path.exists():
        print("📁 Global virtual environment already exists at ./venv")
        return True

    print("🔧 Creating global virtual environment...")

    # Create virtual environment
    success, stdout, stderr = run_command(f"{sys.executable} -m venv venv")

    if not success:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False

    print("✅ Global virtual environment created at ./venv")
    return True


def create_project_venvs():
    """Create individual virtual environments for each project"""
    projects_dir = Path("projects")
    if not projects_dir.exists():
        print("❌ Projects directory not found!")
        return False

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    if not projects:
        print("❌ No projects found!")
        return False

    success_count = 0

    for project_name in projects:
        project_path = projects_dir / project_name
        venv_path = project_path / "venv"

        if not project_path.exists():
            print(f"⚠️  Project {project_name} not found, skipping...")
            continue

        if venv_path.exists():
            print(f"📁 {project_name}: Virtual environment already exists")
            success_count += 1
            continue

        print(f"🔧 {project_name}: Creating virtual environment...")

        success, stdout, stderr = run_command(
            f"{sys.executable} -m venv venv", cwd=project_path
        )

        if success:
            print(f"✅ {project_name}: Virtual environment created")
            success_count += 1
        else:
            print(f"❌ {project_name}: Failed to create virtual environment: {stderr}")

    print(f"\n📊 Summary: {success_count}/{len(projects)} virtual environments ready")
    return success_count == len(projects)


def install_dependencies_in_venv(mode="global"):
    """Install dependencies in virtual environment(s)"""
    if mode == "global":
        return install_global_dependencies()
    elif mode == "individual":
        return install_individual_dependencies()
    else:
        print("❌ Invalid mode. Use 'global' or 'individual'")
        return False


def install_global_dependencies():
    """Install all dependencies in the global virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Global virtual environment not found. Run setup first.")
        return False

    # Determine pip path based on OS
    if os.name == "nt":  # Windows
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix-like
        pip_path = venv_path / "bin" / "pip"

    print("📦 Installing dependencies in global virtual environment...")

    # Collect all requirements
    projects_dir = Path("projects")
    all_requirements = set()

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    for project_name in projects:
        req_file = projects_dir / project_name / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text().strip()
            if content and not content.startswith("#"):
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        all_requirements.add(line)

    if not all_requirements:
        print("ℹ️  No external dependencies found")
        return True

    # Install requirements
    for requirement in sorted(all_requirements):
        print(f"📥 Installing {requirement}...")
        success, stdout, stderr = run_command(f'"{pip_path}" install "{requirement}"')

        if success:
            print(f"✅ {requirement} installed successfully")
        else:
            print(f"❌ Failed to install {requirement}: {stderr}")
            return False

    print("🎉 All dependencies installed in global virtual environment!")
    return True


def install_individual_dependencies():
    """Install dependencies in individual project virtual environments"""
    projects_dir = Path("projects")

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    success_count = 0

    for project_name in projects:
        project_path = projects_dir / project_name
        venv_path = project_path / "venv"
        req_file = project_path / "requirements.txt"

        if not project_path.exists():
            continue

        if not venv_path.exists():
            print(f"❌ {project_name}: Virtual environment not found")
            continue

        # Determine pip path based on OS
        if os.name == "nt":  # Windows
            pip_path = venv_path / "Scripts" / "pip"
        else:  # Unix-like
            pip_path = venv_path / "bin" / "pip"

        if not req_file.exists():
            print(f"ℹ️  {project_name}: No requirements.txt found")
            success_count += 1
            continue

        content = req_file.read_text().strip()
        if not content or content.startswith("#"):
            print(f"ℹ️  {project_name}: No dependencies needed")
            success_count += 1
            continue

        print(f"📦 {project_name}: Installing dependencies...")

        success, stdout, stderr = run_command(f'"{pip_path}" install -r "{req_file}"')

        if success:
            print(f"✅ {project_name}: Dependencies installed successfully")
            success_count += 1
        else:
            print(f"❌ {project_name}: Failed to install dependencies: {stderr}")

    print(
        f"\n📊 Summary: {success_count}/{len(projects)} projects have dependencies ready"
    )
    return success_count > 0


def main():
    print("🐍 Virtual Environment Setup")
    print("=" * 40)

    if not check_python_version():
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python tools/setup-venv.py <command> [options]")
        print("\nCommands:")
        print("  create-global      - Create global virtual environment")
        print("  create-individual  - Create individual project virtual environments")
        print("  install-global     - Install all dependencies in global venv")
        print("  install-individual - Install dependencies in individual venvs")
        print("  setup-global       - Complete global setup (create + install)")
        print("  setup-individual   - Complete individual setup (create + install)")
        print("\nExamples:")
        print("  python tools/setup-venv.py setup-global")
        print("  python tools/setup-venv.py create-individual")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create-global":
        success = create_global_venv()
    elif command == "create-individual":
        success = create_project_venvs()
    elif command == "install-global":
        success = install_dependencies_in_venv("global")
    elif command == "install-individual":
        success = install_dependencies_in_venv("individual")
    elif command == "setup-global":
        print("🚀 Setting up global virtual environment...")
        success = create_global_venv() and install_dependencies_in_venv("global")
        if success:
            print("\n🎉 Global virtual environment setup complete!")
            print(
                "💡 Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
            )
    elif command == "setup-individual":
        print("🚀 Setting up individual virtual environments...")
        success = create_project_venvs() and install_dependencies_in_venv("individual")
        if success:
            print("\n🎉 Individual virtual environments setup complete!")
            print("💡 Use: source projects/PROJECT_NAME/venv/bin/activate")
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

    if not success:
        print("\n⚠️  Setup completed with some errors. Check messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
