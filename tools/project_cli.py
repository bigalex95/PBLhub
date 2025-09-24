#!/usr/bin/env python3
"""
Project Management CLI
Simple command-line interface for managing projects
"""

import sys
from pathlib import Path
from project_config import ProjectConfig, get_projects


def list_projects():
    """List all projects with detailed information"""
    config = ProjectConfig()
    config.print_projects_summary()


def add_project(project_name: str):
    """Add a new project"""
    if not project_name:
        print("❌ Project name is required")
        return False

    # Validate project name format
    if not project_name.replace("-", "").replace("_", "").isalnum():
        print(
            "❌ Project name should contain only letters, numbers, hyphens, and underscores"
        )
        return False

    projects_dir = Path("projects")
    project_path = projects_dir / project_name

    if project_path.exists():
        print(f"❌ Project {project_name} already exists")
        return False

    # Create project directory and basic files
    try:
        project_path.mkdir(parents=True)

        # Create main.py
        main_content = f'''#!/usr/bin/env python3
"""
{project_name.replace('-', ' ').replace('_', ' ').title()}
Learning project for Python development
"""

def main():
    """Main function"""
    print(f"🐍 {project_name.replace('-', ' ').replace('_', ' ').title()}")
    print("Project setup complete!")
    
    # TODO: Implement project functionality
    pass

if __name__ == "__main__":
    main()
'''
        (project_path / "main.py").write_text(main_content)

        # Create requirements.txt
        req_content = f"""# Dependencies for {project_name}
# Add your project dependencies here
# Example:
# requests>=2.25.0
# beautifulsoup4>=4.9.0
"""
        (project_path / "requirements.txt").write_text(req_content)

        print(f"✅ Created project {project_name}")
        print(f"📁 Project directory: projects/{project_name}/")
        print(f"🐍 Main file: projects/{project_name}/main.py")
        print(f"📦 Requirements: projects/{project_name}/requirements.txt")

        # Update project configuration
        config = ProjectConfig()
        config.add_project(project_name)

        print("💡 Next steps:")
        print(f"  1. Edit projects/{project_name}/main.py")
        print(f"  2. Add dependencies to projects/{project_name}/requirements.txt")
        print(
            "  3. Set up virtual environment: python tools/setup-venv.py setup-global"
        )
        print("  4. Install dependencies: python tools/install-deps.py")

        return True

    except Exception as e:
        print(f"❌ Failed to create project: {e}")
        # Clean up on failure
        if project_path.exists():
            import shutil

            shutil.rmtree(project_path)
        return False


def remove_project(project_name: str):
    """Remove a project (with confirmation)"""
    if not project_name:
        print("❌ Project name is required")
        return False

    projects_dir = Path("projects")
    project_path = projects_dir / project_name

    if not project_path.exists():
        print(f"❌ Project {project_name} does not exist")
        return False

    # Confirm deletion
    print(f"⚠️  This will permanently delete the project '{project_name}'")
    print(f"📁 Location: {project_path}")

    response = input("Are you sure? Type 'yes' to confirm: ")

    if response.lower() != "yes":
        print("❌ Operation cancelled")
        return False

    try:
        import shutil

        shutil.rmtree(project_path)

        # Update project configuration
        config = ProjectConfig()
        config.remove_project(project_name)

        print(f"✅ Removed project {project_name}")
        return True

    except Exception as e:
        print(f"❌ Failed to remove project: {e}")
        return False


def show_project_info(project_name: str):
    """Show detailed information about a project"""
    if not project_name:
        print("❌ Project name is required")
        return False

    config = ProjectConfig()
    project_info = config.get_project_info(project_name)

    if not project_info:
        print(f"❌ Project {project_name} not found")
        return False

    print(f"📋 Project Information: {project_name}")
    print("=" * 50)

    for key, value in project_info.items():
        if key == "name":
            print(f"📁 Name: {value}")
        elif key == "path":
            print(f"📍 Path: {value}")
        elif key == "description" and value:
            print(f"📝 Description: {value}")
        elif key.startswith("has_"):
            feature = key[4:].replace("_", " ").title()
            status = "✅ Yes" if value else "❌ No"
            print(f"{feature}: {status}")

    return True


def refresh_projects():
    """Refresh project list from filesystem"""
    config = ProjectConfig()
    projects = config.get_projects(refresh=True)
    print(f"🔄 Refreshed project list - found {len(projects)} projects")

    for project in projects:
        print(f"  📁 {project['name']}")


def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print("🛠️  Project Management CLI")
        print("=" * 30)
        print("Usage: python tools/project_cli.py <command> [args]")
        print("")
        print("Commands:")
        print("  list                    - List all projects")
        print("  add <project_name>      - Add a new project")
        print("  remove <project_name>   - Remove a project")
        print("  info <project_name>     - Show project information")
        print("  refresh                 - Refresh project list from filesystem")
        print("")
        print("Examples:")
        print("  python tools/project_cli.py list")
        print("  python tools/project_cli.py add 09-new-project")
        print("  python tools/project_cli.py info 01-file-organizer")
        print("  python tools/project_cli.py remove 09-new-project")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_projects()
    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ Project name is required for 'add' command")
            sys.exit(1)
        project_name = sys.argv[2]
        if not add_project(project_name):
            sys.exit(1)
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Project name is required for 'remove' command")
            sys.exit(1)
        project_name = sys.argv[2]
        if not remove_project(project_name):
            sys.exit(1)
    elif command == "info":
        if len(sys.argv) < 3:
            print("❌ Project name is required for 'info' command")
            sys.exit(1)
        project_name = sys.argv[2]
        if not show_project_info(project_name):
            sys.exit(1)
    elif command == "refresh":
        refresh_projects()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
