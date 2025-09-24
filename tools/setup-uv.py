#!/usr/bin/env python3
"""
UV Setup and Management Script
This script sets up UV (ultra-fast Python package installer) for projects
UV is a modern replacement for pip and virtualenv written in Rust
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
import json


# Import centralized project configuration
def get_projects_config():
    """Get project configuration with proper error handling"""
    try:
        # Try relative import first
        from .project_config import get_project_names, get_project_paths, ProjectConfig

        return get_project_names, get_project_paths, ProjectConfig
    except ImportError:
        # Handle direct execution
        import importlib.util

        config_path = Path(__file__).parent / "project_config.py"
        if config_path.exists():
            spec = importlib.util.spec_from_file_location("project_config", config_path)
            if spec and spec.loader:
                project_config = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(project_config)
                return (
                    project_config.get_project_names,
                    project_config.get_project_paths,
                    project_config.ProjectConfig,
                )

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

    def fallback_get_project_paths():
        return [f"projects/{name}" for name in fallback_get_project_names()]

    class FallbackProjectConfig:
        def get_project_names(self):
            return fallback_get_project_names()

        def get_project_paths(self):
            return fallback_get_project_paths()

    return fallback_get_project_names, fallback_get_project_paths, FallbackProjectConfig


def run_command(cmd, cwd=None):
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_uv_installed():
    """Check if UV is installed"""
    success, stdout, stderr = run_command("uv --version")
    if success:
        version = stdout.strip()
        print(f"✅ UV is installed: {version}")
        return True
    else:
        print("❌ UV is not installed")
        return False


def install_uv():
    """Install UV package manager"""
    print("🚀 Installing UV package manager...")

    # Try different installation methods
    install_commands = [
        "pip install uv",
        "pipx install uv",
        "curl -LsSf https://astral.sh/uv/install.sh | sh",
    ]

    for cmd in install_commands:
        print(f"🔧 Trying: {cmd}")
        success, stdout, stderr = run_command(cmd)

        if success and check_uv_installed():
            print("✅ UV installed successfully!")
            return True
        else:
            print(f"⚠️  Command failed: {stderr}")

    print("❌ Failed to install UV. Please install manually:")
    print("   - Visit: https://docs.astral.sh/uv/getting-started/installation/")
    print("   - Or run: pip install uv")
    return False


def create_pyproject_toml(project_path, project_name):
    """Create pyproject.toml file for UV project management"""
    pyproject_path = project_path / "pyproject.toml"

    if pyproject_path.exists():
        print(f"📁 {project_name}: pyproject.toml already exists")
        return True

    # Read existing requirements.txt if available
    req_file = project_path / "requirements.txt"
    dependencies = []

    if req_file.exists():
        content = req_file.read_text().strip()
        if content and not content.startswith("#"):
            for line in content.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    dependencies.append(f'"{line}"')

    # Create pyproject.toml content
    deps_str = ",\n    ".join(dependencies) if dependencies else ""

    pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "Learning project: {project_name.replace('-', ' ').title()}"
dependencies = [
    {deps_str}
]
requires-python = ">=3.8"

[project.scripts]
{project_name.replace('-', '_')} = "main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=5.0",
]
"""

    try:
        pyproject_path.write_text(pyproject_content)
        print(f"✅ {project_name}: Created pyproject.toml")
        return True
    except Exception as e:
        print(f"❌ {project_name}: Failed to create pyproject.toml: {e}")
        return False


def setup_uv_project(project_path, project_name):
    """Setup UV for a single project"""
    print(f"🔧 {project_name}: Setting up UV project...")

    # Create pyproject.toml
    if not create_pyproject_toml(project_path, project_name):
        return False

    # Initialize UV project
    success, stdout, stderr = run_command("uv sync", cwd=project_path)

    if success:
        print(f"✅ {project_name}: UV project initialized and dependencies synced")
        return True
    else:
        print(f"❌ {project_name}: UV sync failed: {stderr}")
        return False


def setup_all_uv_projects():
    """Setup UV for all projects"""
    projects_dir = Path("projects")
    if not projects_dir.exists():
        print("❌ Projects directory not found!")
        return False

    # Get projects dynamically
    get_project_names, _, _ = get_projects_config()
    projects = get_project_names()

    if not projects:
        print("❌ No projects found!")
        return False

    success_count = 0

    for project_name in projects:
        project_path = projects_dir / project_name

        if not project_path.exists():
            print(f"⚠️  Project {project_name} not found, skipping...")
            continue

        if setup_uv_project(project_path, project_name):
            success_count += 1

    print(f"\n📊 UV Setup Summary: {success_count}/{len(projects)} projects configured")
    return success_count > 0


def create_uv_workspace():
    """Create UV workspace configuration"""
    workspace_file = Path("uv.toml")

    if workspace_file.exists():
        print("📁 UV workspace configuration already exists")
        return True

    # Get projects dynamically
    _, get_project_paths, _ = get_projects_config()
    project_paths = get_project_paths()

    # Format project paths for TOML
    members_list = ",\n    ".join(f'"{path}"' for path in project_paths)

    workspace_content = f"""# UV Workspace Configuration
[workspace]
members = [
    {members_list},
]

[workspace.dependencies]
# Shared development dependencies
pytest = ">=7.0"
black = ">=23.0"
flake8 = ">=5.0"
mypy = ">=1.0"

[tool.uv]
# Global UV settings
python-preference = "managed"
"""

    try:
        workspace_file.write_text(workspace_content)
        print("✅ Created UV workspace configuration (uv.toml)")
        return True
    except Exception as e:
        print(f"❌ Failed to create UV workspace configuration: {e}")
        return False


def run_uv_command(command, project_name=None):
    """Run UV command in project or workspace"""
    if project_name:
        project_path = Path("projects") / project_name
        if not project_path.exists():
            print(f"❌ Project {project_name} not found")
            return False

        success, stdout, stderr = run_command(f"uv {command}", cwd=project_path)
        if success:
            print(f"✅ {project_name}: {command} completed")
            if stdout:
                print(stdout)
        else:
            print(f"❌ {project_name}: {command} failed: {stderr}")
        return success
    else:
        # Run in workspace root
        success, stdout, stderr = run_command(f"uv {command}")
        if success:
            print(f"✅ Workspace: {command} completed")
            if stdout:
                print(stdout)
        else:
            print(f"❌ Workspace: {command} failed: {stderr}")
        return success


def main():
    print("⚡ UV Setup and Management")
    print("=" * 30)

    if len(sys.argv) < 2:
        print("Usage: python tools/setup-uv.py <command> [project_name]")
        print("\nCommands:")
        print("  install            - Install UV package manager")
        print("  check              - Check if UV is installed")
        print("  init-workspace     - Initialize UV workspace")
        print("  setup-all          - Setup UV for all projects")
        print("  setup-project      - Setup UV for specific project")
        print("  sync [project]     - Sync dependencies (project or workspace)")
        print("  run [project]      - Run project with UV")
        print("  add <pkg> [proj]   - Add package to project")
        print("  remove <pkg> [proj] - Remove package from project")
        print("\nExamples:")
        print("  python tools/setup-uv.py install")
        print("  python tools/setup-uv.py setup-all")
        print("  python tools/setup-uv.py sync 01-file-organizer")
        print("  python tools/setup-uv.py add requests 04-web-scraper")
        sys.exit(1)

    command = sys.argv[1]

    if command == "install":
        install_uv()
    elif command == "check":
        check_uv_installed()
    elif command == "init-workspace":
        if check_uv_installed():
            create_uv_workspace()
        else:
            print("❌ UV not installed. Run 'install' command first.")
    elif command == "setup-all":
        if not check_uv_installed():
            if not install_uv():
                sys.exit(1)

        print("🚀 Setting up UV for all projects...")
        create_uv_workspace()
        setup_all_uv_projects()
        print("\n🎉 UV setup complete!")
        print("💡 Usage examples:")
        print("  uv sync                          # Sync workspace")
        print("  uv run --directory projects/01-file-organizer python main.py")
        print("  uv add --directory projects/04-web-scraper requests")

    elif command == "setup-project":
        if len(sys.argv) < 3:
            print("❌ Please specify project name")
            sys.exit(1)

        project_name = sys.argv[2]
        if not check_uv_installed():
            print("❌ UV not installed. Run 'install' command first.")
            sys.exit(1)

        project_path = Path("projects") / project_name
        setup_uv_project(project_path, project_name)

    elif command == "sync":
        if not check_uv_installed():
            print("❌ UV not installed")
            sys.exit(1)

        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        run_uv_command("sync", project_name)

    elif command == "run":
        if len(sys.argv) < 3:
            print("❌ Please specify project name")
            sys.exit(1)

        if not check_uv_installed():
            print("❌ UV not installed")
            sys.exit(1)

        project_name = sys.argv[2]
        run_uv_command("run python main.py", project_name)

    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ Please specify package name")
            sys.exit(1)

        if not check_uv_installed():
            print("❌ UV not installed")
            sys.exit(1)

        package = sys.argv[2]
        project_name = sys.argv[3] if len(sys.argv) > 3 else None

        if project_name:
            run_uv_command(f"add {package}", project_name)
        else:
            # Add to workspace
            run_uv_command(f"add {package}")

    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Please specify package name")
            sys.exit(1)

        if not check_uv_installed():
            print("❌ UV not installed")
            sys.exit(1)

        package = sys.argv[2]
        project_name = sys.argv[3] if len(sys.argv) > 3 else None

        if project_name:
            run_uv_command(f"remove {package}", project_name)
        else:
            run_uv_command(f"remove {package}")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
