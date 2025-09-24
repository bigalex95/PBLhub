#!/usr/bin/env python3
"""
Project Configuration Module
Centralized project discovery and management for PBLhub
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import json


class ProjectConfig:
    """Central project configuration and discovery"""

    def __init__(self, workspace_root: Optional[str] = None):
        """Initialize with workspace root directory"""
        if workspace_root is None:
            # Auto-detect workspace root
            current = Path.cwd()
            while current != current.parent:
                if (current / "projects").exists():
                    workspace_root = str(current)
                    break
                current = current.parent
            else:
                workspace_root = str(Path.cwd())

        self.workspace_root = Path(workspace_root)
        self.projects_dir = self.workspace_root / "projects"
        self.config_file = self.workspace_root / "tools" / "project_config.json"

    def discover_projects(self) -> List[Dict[str, str]]:
        """Auto-discover all projects in the projects directory"""
        projects = []

        if not self.projects_dir.exists():
            return projects

        for item in sorted(self.projects_dir.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                # Check if it looks like a project (has main.py or requirements.txt)
                main_py = item / "main.py"
                requirements_txt = item / "requirements.txt"

                if main_py.exists() or requirements_txt.exists():
                    # Extract project info
                    project_info = {
                        "name": item.name,
                        "path": str(item.relative_to(self.workspace_root)),
                        "full_path": str(item),
                        "has_main": main_py.exists(),
                        "has_requirements": requirements_txt.exists(),
                        "has_venv": (item / "venv").exists(),
                        "has_pyproject": (item / "pyproject.toml").exists(),
                    }

                    # Try to extract description from main.py or README
                    description = self._extract_description(item)
                    if description:
                        project_info["description"] = description

                    projects.append(project_info)

        return projects

    def _extract_description(self, project_path: Path) -> Optional[str]:
        """Extract project description from main.py docstring or README"""
        # Try main.py first
        main_py = project_path / "main.py"
        if main_py.exists():
            try:
                content = main_py.read_text(encoding="utf-8")
                lines = content.split("\n")

                # Look for docstring or print statement with description
                for i, line in enumerate(lines[:20]):  # Check first 20 lines
                    if "print(" in line and ("Learning" in line or "Project" in line):
                        # Extract from print statement
                        start = line.find('"') or line.find("'")
                        if start != -1:
                            quote_char = line[start]
                            end = line.find(quote_char, start + 1)
                            if end != -1:
                                return line[start + 1 : end]

                    # Look for module docstring
                    if line.strip().startswith('"""') or line.strip().startswith("'''"):
                        quote_type = '"""' if '"""' in line else "'''"
                        if line.strip().endswith(quote_type) and len(line.strip()) > 6:
                            # Single line docstring
                            return line.strip()[3:-3].strip()
                        else:
                            # Multi-line docstring
                            for j in range(i + 1, min(i + 5, len(lines))):
                                if quote_type in lines[j]:
                                    desc_lines = lines[i : j + 1]
                                    desc = (
                                        " ".join(desc_lines)
                                        .replace(quote_type, "")
                                        .strip()
                                    )
                                    return (
                                        desc[:100] + "..." if len(desc) > 100 else desc
                                    )

            except Exception:
                pass

        # Try README if main.py doesn't have description
        for readme_name in ["README.md", "README.txt", "readme.md", "readme.txt"]:
            readme_path = project_path / readme_name
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    lines = [
                        line.strip() for line in content.split("\n") if line.strip()
                    ]
                    if lines:
                        # Return first non-header line
                        for line in lines[:5]:
                            if not line.startswith("#") and len(line) > 10:
                                return line[:100] + "..." if len(line) > 100 else line
                except Exception:
                    pass

        return None

    def get_projects(self, refresh: bool = False) -> List[Dict[str, str]]:
        """Get list of projects, with optional refresh from filesystem"""
        if refresh or not self.config_file.exists():
            projects = self.discover_projects()
            self.save_config(projects)
            return projects
        else:
            return self.load_config()

    def get_project_names(self, refresh: bool = False) -> List[str]:
        """Get list of project names only"""
        projects = self.get_projects(refresh=refresh)
        return [project["name"] for project in projects]

    def get_project_paths(self, refresh: bool = False) -> List[str]:
        """Get list of project paths relative to workspace root"""
        projects = self.get_projects(refresh=refresh)
        return [project["path"] for project in projects]

    def get_project_full_paths(self, refresh: bool = False) -> List[Path]:
        """Get list of full project paths"""
        projects = self.get_projects(refresh=refresh)
        return [Path(project["full_path"]) for project in projects]

    def save_config(self, projects: List[Dict[str, str]]) -> None:
        """Save project configuration to JSON file"""
        config_data = {
            "version": "1.0",
            "workspace_root": str(self.workspace_root),
            "projects": projects,
            "last_updated": str(Path(__file__).stat().st_mtime),
        }

        # Ensure tools directory exists
        self.config_file.parent.mkdir(exist_ok=True)

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save project config: {e}")

    def load_config(self) -> List[Dict[str, str]]:
        """Load project configuration from JSON file"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                return config_data.get("projects", [])
        except Exception as e:
            print(f"Warning: Could not load project config: {e}")
            # Fall back to auto-discovery
            return self.discover_projects()

    def add_project(self, project_name: str, force_refresh: bool = True) -> bool:
        """Add a new project and refresh configuration"""
        project_path = self.projects_dir / project_name

        if not project_path.exists():
            print(f"Project directory {project_name} does not exist")
            return False

        # Refresh configuration to include new project
        projects = self.discover_projects()
        self.save_config(projects)

        return any(p["name"] == project_name for p in projects)

    def remove_project(self, project_name: str) -> bool:
        """Remove project from configuration (does not delete files)"""
        projects = self.load_config()
        original_count = len(projects)
        projects = [p for p in projects if p["name"] != project_name]

        if len(projects) < original_count:
            self.save_config(projects)
            return True
        return False

    def get_project_info(self, project_name: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a specific project"""
        projects = self.get_projects()
        for project in projects:
            if project["name"] == project_name:
                return project
        return None

    def print_projects_summary(self) -> None:
        """Print a summary of all projects"""
        projects = self.get_projects(refresh=True)

        print(f"📁 Found {len(projects)} projects in {self.projects_dir}")
        print("=" * 50)

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

            status = " ".join(status_icons) if status_icons else "📝"

            print(f"{status} {project['name']}")
            if project.get("description"):
                print(f"   {project['description']}")
            print()


# Convenience functions for easy import
def get_projects(refresh: bool = False) -> List[Dict[str, str]]:
    """Get all projects"""
    config = ProjectConfig()
    return config.get_projects(refresh=refresh)


def get_project_names(refresh: bool = False) -> List[str]:
    """Get all project names"""
    config = ProjectConfig()
    return config.get_project_names(refresh=refresh)


def get_project_paths(refresh: bool = False) -> List[str]:
    """Get all project paths"""
    config = ProjectConfig()
    return config.get_project_paths(refresh=refresh)


def refresh_projects() -> List[Dict[str, str]]:
    """Force refresh project list from filesystem"""
    config = ProjectConfig()
    return config.get_projects(refresh=True)


# Main execution for testing
if __name__ == "__main__":
    config = ProjectConfig()
    config.print_projects_summary()
