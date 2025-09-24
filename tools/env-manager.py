#!/usr/bin/env python3
"""
Environment Management Script
Comprehensive tool for managing Python environments across all projects
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
    """Check Python version and environment"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    print(f"📍 Executable: {sys.executable}")

    # Check if running in virtual environment
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("🔧 Currently in virtual environment")
    else:
        print("🌐 Using system Python")

    return True


def check_environment_status():
    """Check status of all environments"""
    print("🔍 Environment Status Check")
    print("=" * 40)

    # Check global venv
    global_venv = Path("venv")
    if global_venv.exists():
        print("✅ Global virtual environment: EXISTS")

        # Check if it has packages
        site_packages = global_venv / "lib" / "python*" / "site-packages"
        if list(Path(".").glob(str(site_packages))):
            print("📦 Global venv has packages installed")
        else:
            print("📭 Global venv is empty")
    else:
        print("❌ Global virtual environment: NOT FOUND")

    print()

    # Check UV
    uv_installed, _, _ = run_command("uv --version")
    if uv_installed:
        print("✅ UV package manager: INSTALLED")

        # Check for UV workspace
        if Path("uv.toml").exists():
            print("✅ UV workspace: CONFIGURED")
        else:
            print("⚠️  UV workspace: NOT CONFIGURED")
    else:
        print("❌ UV package manager: NOT INSTALLED")

    print()

    # Check individual project environments
    projects_dir = Path("projects")

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    print("📁 Individual Project Environments:")
    venv_count = 0
    pyproject_count = 0

    for project in projects:
        project_path = projects_dir / project
        if not project_path.exists():
            continue

        venv_exists = (project_path / "venv").exists()
        pyproject_exists = (project_path / "pyproject.toml").exists()

        status_parts = []
        if venv_exists:
            status_parts.append("venv")
            venv_count += 1
        if pyproject_exists:
            status_parts.append("UV")
            pyproject_count += 1

        if status_parts:
            print(f"  ✅ {project}: {', '.join(status_parts)}")
        else:
            print(f"  ❌ {project}: No environment")

    print(
        f"\n📊 Summary: {venv_count}/{len(projects)} have venv, {pyproject_count}/{len(projects)} have UV config"
    )


def setup_recommended_environment():
    """Setup the recommended environment configuration"""
    print("🚀 Setting up recommended environment configuration...")
    print("=" * 50)

    print("Step 1: Creating global virtual environment...")
    success, stdout, stderr = run_command("python3 tools/setup-venv.py setup-global")
    if not success:
        print(f"❌ Failed to setup global venv: {stderr}")
        return False

    print("\nStep 2: Setting up UV (optional but recommended)...")
    success, stdout, stderr = run_command("python3 tools/setup-uv.py setup-all")
    if not success:
        print("⚠️  UV setup failed, but continuing with venv setup")
        print(f"   Error: {stderr}")

    print("\n✅ Recommended environment setup complete!")
    print("\n💡 Next steps:")
    print("1. Activate the environment:")
    print("   source venv/bin/activate")
    print("2. Install dependencies:")
    print("   python tools/install-deps.py")
    print("3. Run projects:")
    print("   python tools/run-all.py")

    return True


def cleanup_environments():
    """Clean up all environments"""
    print("🧹 Cleaning up environments...")

    # Remove global venv
    global_venv = Path("venv")
    if global_venv.exists():
        success, _, _ = run_command("rm -rf venv")
        if success:
            print("✅ Removed global virtual environment")
        else:
            print("❌ Failed to remove global virtual environment")

    # Remove project venvs
    projects_dir = Path("projects")
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            venv_dir = project_dir / "venv"
            if venv_dir.exists():
                success, _, _ = run_command(f"rm -rf {venv_dir}")
                if success:
                    print(f"✅ Removed {project_dir.name}/venv")

    # Remove UV files
    uv_files = ["uv.toml", "uv.lock"]
    for uv_file in uv_files:
        if Path(uv_file).exists():
            Path(uv_file).unlink()
            print(f"✅ Removed {uv_file}")

    # Remove pyproject.toml files
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            pyproject_file = project_dir / "pyproject.toml"
            if pyproject_file.exists():
                pyproject_file.unlink()
                print(f"✅ Removed {project_dir.name}/pyproject.toml")

    print("🎉 Environment cleanup complete!")


def show_usage_examples():
    """Show usage examples for different environments"""
    print("💡 Environment Usage Examples")
    print("=" * 35)

    # Get a sample project for examples
    get_project_names, _ = get_projects_config()
    projects = get_project_names()
    example_project = projects[0] if projects else "01-file-organizer"
    example_web_project = next(
        (p for p in projects if "web" in p or "scraper" in p),
        projects[1] if len(projects) > 1 else "04-web-scraper",
    )

    print("\n🌐 Global Virtual Environment:")
    print("  # Activate")
    print("  source venv/bin/activate")
    print("  # Install dependencies")
    print("  python tools/install-deps.py")
    print("  # Run projects")
    print(f"  python projects/{example_project}/main.py")
    print("  # Deactivate")
    print("  deactivate")

    print("\n📁 Individual Project Virtual Environments:")
    print("  # Activate specific project")
    print(f"  source projects/{example_project}/venv/bin/activate")
    print("  # Run project")
    print(f"  cd projects/{example_project} && python main.py")

    print("\n⚡ UV Package Manager:")
    print("  # Sync all dependencies")
    print("  uv sync")
    print("  # Run specific project")
    print(f"  uv run --directory projects/{example_project} python main.py")
    print("  # Add package to project")
    print(f"  uv add --directory projects/{example_web_project} requests")

    print("\n🛠️ Management Commands:")
    print("  # Setup environments")
    print("  python tools/env-manager.py setup")
    print("  # Check status")
    print("  python tools/env-manager.py status")
    print("  # Clean up")
    print("  python tools/env-manager.py cleanup")


def main():
    print("🔧 Environment Manager")
    print("=" * 25)

    if len(sys.argv) < 2:
        print("Usage: python tools/env-manager.py <command>")
        print("\nCommands:")
        print("  status    - Check environment status")
        print("  setup     - Setup recommended environment")
        print("  cleanup   - Clean up all environments")
        print("  examples  - Show usage examples")
        print("  version   - Show Python version info")
        print("\nExamples:")
        print("  python tools/env-manager.py status")
        print("  python tools/env-manager.py setup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        check_environment_status()
    elif command == "setup":
        setup_recommended_environment()
    elif command == "cleanup":
        cleanup_environments()
    elif command == "examples":
        show_usage_examples()
    elif command == "version":
        check_python_version()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
