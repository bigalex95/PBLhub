#!/usr/bin/env python3
"""
Documentation Updater Script
Automatically updates README and documentation files with current project list
"""

import re
from pathlib import Path
from typing import List, Dict
from project_config import ProjectConfig, get_projects


def update_readme_project_list():
    """Update the main README.md with current project list"""
    readme_path = Path("README.md")

    if not readme_path.exists():
        print("❌ README.md not found")
        return False

    # Get current projects
    projects = get_projects(refresh=True)

    # Generate project list markdown
    project_list_md = generate_project_list_markdown(projects)

    # Read current README
    content = readme_path.read_text(encoding="utf-8")

    # Find and replace project list section
    # Look for markers like <!-- PROJECT_LIST_START --> and <!-- PROJECT_LIST_END -->
    start_marker = "<!-- PROJECT_LIST_START -->"
    end_marker = "<!-- PROJECT_LIST_END -->"

    if start_marker in content and end_marker in content:
        # Replace existing section
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker) + len(end_marker)

        new_section = f"{start_marker}\n{project_list_md}\n{end_marker}"
        new_content = content[:start_idx] + new_section + content[end_idx:]

        readme_path.write_text(new_content, encoding="utf-8")
        print("✅ Updated README.md project list")
        return True
    else:
        print("⚠️  README.md doesn't have project list markers")
        print(
            "💡 Add <!-- PROJECT_LIST_START --> and <!-- PROJECT_LIST_END --> markers"
        )
        return False


def generate_project_list_markdown(projects: List[Dict[str, str]]) -> str:
    """Generate markdown for project list"""
    lines = ["## 📁 Projects"]
    lines.append("")

    for i, project in enumerate(projects, 1):
        name = project["name"]
        description = project.get("description", "Learning project")

        # Create badges for project status
        badges = []
        if project.get("has_main"):
            badges.append("![Python](https://img.shields.io/badge/Python-✓-green)")
        if project.get("has_requirements"):
            badges.append("![Deps](https://img.shields.io/badge/Dependencies-✓-blue)")
        if project.get("has_venv"):
            badges.append("![Venv](https://img.shields.io/badge/Venv-✓-orange)")
        if project.get("has_pyproject"):
            badges.append("![UV](https://img.shields.io/badge/UV-✓-purple)")

        badge_str = " ".join(badges) if badges else ""

        lines.append(f"### {i:02d}. {name.replace('-', ' ').title()}")
        if badge_str:
            lines.append(f"{badge_str}")
        lines.append(f"**Path:** `projects/{name}/`")
        if description:
            lines.append(f"**Description:** {description}")
        lines.append("")
        lines.append(f"```bash")
        lines.append(f"# Run the project")
        lines.append(f"python projects/{name}/main.py")
        lines.append(f"```")
        lines.append("")

    return "\\n".join(lines)


def update_build_setup_docs():
    """Update BUILD_SETUP.md with current project information"""
    build_setup_path = Path("BUILD_SETUP.md")

    if not build_setup_path.exists():
        print("❌ BUILD_SETUP.md not found")
        return False

    projects = get_projects(refresh=True)
    project_count = len(projects)

    content = build_setup_path.read_text(encoding="utf-8")

    # Update project count references
    content = re.sub(
        r"All \d+ Python projects", f"All {project_count} Python projects", content
    )
    content = re.sub(r"\d+ projects", f"{project_count} projects", content)

    build_setup_path.write_text(content, encoding="utf-8")
    print(f"✅ Updated BUILD_SETUP.md with {project_count} projects")
    return True


def update_virtual_env_guide():
    """Update VIRTUAL_ENV_GUIDE.md with current project examples"""
    guide_path = Path("VIRTUAL_ENV_GUIDE.md")

    if not guide_path.exists():
        print("❌ VIRTUAL_ENV_GUIDE.md not found")
        return False

    projects = get_projects(refresh=True)

    if not projects:
        print("⚠️  No projects found for guide update")
        return False

    # Get example projects for different purposes
    example_project = projects[0]["name"]
    web_project = next(
        (p["name"] for p in projects if "web" in p["name"] or "scraper" in p["name"]),
        projects[1]["name"] if len(projects) > 1 else example_project,
    )

    content = guide_path.read_text(encoding="utf-8")

    # Update project examples (this is a simple approach, could be more sophisticated)
    content = re.sub(
        r"projects/01-file-organizer", f"projects/{example_project}", content
    )
    content = re.sub(r"projects/04-web-scraper", f"projects/{web_project}", content)

    guide_path.write_text(content, encoding="utf-8")
    print("✅ Updated VIRTUAL_ENV_GUIDE.md with current project examples")
    return True


def update_uv_workspace():
    """Update uv.toml workspace with current projects"""
    uv_toml_path = Path("uv.toml")

    if not uv_toml_path.exists():
        print("ℹ️  uv.toml not found (will be created when UV is set up)")
        return True

    projects = get_projects(refresh=True)
    project_paths = [f"projects/{p['name']}" for p in projects]

    content = uv_toml_path.read_text(encoding="utf-8")

    # Find the members section and update it
    members_pattern = r"members = \[([^\\]]*?)\\]"
    members_list = ",\\n    ".join(f'"{path}"' for path in project_paths)
    new_members = f"members = [\\n    {members_list},\\n]"

    content = re.sub(members_pattern, new_members, content, flags=re.DOTALL)

    uv_toml_path.write_text(content, encoding="utf-8")
    print(f"✅ Updated uv.toml with {len(projects)} project members")
    return True


def generate_project_summary():
    """Generate a summary of all projects"""
    projects = get_projects(refresh=True)

    print("\\n📊 Project Summary Report")
    print("=" * 50)
    print(f"Total Projects: {len(projects)}")

    # Count by status
    with_main = sum(1 for p in projects if p.get("has_main"))
    with_deps = sum(1 for p in projects if p.get("has_requirements"))
    with_venv = sum(1 for p in projects if p.get("has_venv"))
    with_uv = sum(1 for p in projects if p.get("has_pyproject"))

    print(f"With main.py: {with_main}/{len(projects)}")
    print(f"With requirements.txt: {with_deps}/{len(projects)}")
    print(f"With virtual env: {with_venv}/{len(projects)}")
    print(f"With UV config: {with_uv}/{len(projects)}")

    print("\\n📋 Project List:")
    for project in projects:
        status_icons = []
        if project.get("has_main"):
            status_icons.append("🐍")
        if project.get("has_requirements"):
            status_icons.append("📦")
        if project.get("has_venv"):
            status_icons.append("🔧")
        if project.get("has_pyproject"):
            status_icons.append("⚡")

        status = " ".join(status_icons) or "📝"
        print(f"  {status} {project['name']}")

    return True


def main():
    """Main function"""
    import sys

    print("📝 Documentation Updater")
    print("=" * 30)

    if len(sys.argv) < 2:
        print("Usage: python tools/update_docs.py <command>")
        print("\\nCommands:")
        print("  readme     - Update README.md project list")
        print("  build      - Update BUILD_SETUP.md")
        print("  guide      - Update VIRTUAL_ENV_GUIDE.md")
        print("  uv         - Update uv.toml workspace")
        print("  all        - Update all documentation")
        print("  summary    - Show project summary")
        print("\\nExamples:")
        print("  python tools/update_docs.py all")
        print("  python tools/update_docs.py readme")
        sys.exit(1)

    command = sys.argv[1]

    success = True

    if command == "readme":
        success = update_readme_project_list()
    elif command == "build":
        success = update_build_setup_docs()
    elif command == "guide":
        success = update_virtual_env_guide()
    elif command == "uv":
        success = update_uv_workspace()
    elif command == "all":
        print("🔄 Updating all documentation...")
        success = all(
            [
                update_readme_project_list(),
                update_build_setup_docs(),
                update_virtual_env_guide(),
                update_uv_workspace(),
            ]
        )
        if success:
            print("🎉 All documentation updated successfully!")
    elif command == "summary":
        success = generate_project_summary()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

    if not success:
        print("⚠️  Some operations failed. Check messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
