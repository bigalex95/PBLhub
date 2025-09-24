#!/usr/bin/env python3
"""
Install Dependencies Script
This script installs all dependencies for Python projects
"""

import subprocess
import sys
from pathlib import Path

def install_requirements(project_path):
    """Install requirements for a single project"""
    requirements_file = project_path / "requirements.txt"
    
    if not requirements_file.exists():
        return True, "No requirements.txt found"
    
    # Check if requirements file is just a comment (no real dependencies)
    content = requirements_file.read_text().strip()
    if not content or content.startswith('#'):
        return True, "No dependencies needed"
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            return True, "Dependencies installed successfully"
        else:
            return False, result.stderr.strip() or "Unknown error"
            
    except Exception as e:
        return False, str(e)

def main():
    print("📦 Installing dependencies for all Python projects...")
    print("=" * 60)
    
    # Check if we're in the python branch
    projects_dir = Path("projects")
    if not projects_dir.exists():
        print("❌ Error: projects/ directory not found. Make sure you're in the python branch root.")
        sys.exit(1)
    
    # List of all projects
    projects = [
        "01-file-organizer",
        "02-password-generator", 
        "03-expense-tracker",
        "04-web-scraper",
        "05-api-client",
        "06-task-scheduler",
        "07-data-analyzer",
        "08-mini-framework"
    ]
    
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
        
        success, message = install_requirements(project_path)
        
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
        print("  - Use virtual environment: python -m venv venv && source venv/bin/activate")
        print("  - Check internet connection")
        sys.exit(1)
    else:
        print("🎉 All dependencies installed successfully!")
        print("💡 Next steps:")
        print("  ./tools/run-all.py  # Run all projects")
        print("  python projects/PROJECT_NAME/main.py  # Run individual project")
        sys.exit(0)

if __name__ == "__main__":
    main()