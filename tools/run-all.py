#!/usr/bin/env python3
"""
Run All Python Projects Script
This script runs all projects in the projects/ directory
"""

import subprocess
import sys
from pathlib import Path
import os

def run_project(project_path):
    """Run a single Python project"""
    main_file = project_path / "main.py"
    
    if not main_file.exists():
        return False, f"No main.py found in {project_path.name}"
    
    try:
        # Make the script executable
        os.chmod(main_file, 0o755)
        
        # Run the Python script
        result = subprocess.run(
            [sys.executable, str(main_file)], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or "Unknown error"
            
    except subprocess.TimeoutExpired:
        return False, "Script timeout (30s limit)"
    except Exception as e:
        return False, str(e)

def main():
    print("🐍 Running all Python projects...")
    print("=" * 50)
    
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
    
    successful_projects = []
    failed_projects = []
    
    print("🚀 Running projects individually...")
    print()
    
    # Run each project
    for project_name in projects:
        project_path = projects_dir / project_name
        
        if not project_path.exists():
            print(f"⚠️  Project directory {project_name} not found, skipping...")
            failed_projects.append((project_name, "Directory not found"))
            continue
            
        print(f"🐍 Running {project_name}...")
        
        success, output = run_project(project_path)
        
        if success:
            print(f"✅ {project_name} ran successfully")
            print(f"   Output: {output}")
            successful_projects.append(project_name)
        else:
            print(f"❌ {project_name} failed to run")
            print(f"   Error: {output}")
            failed_projects.append((project_name, output))
        
        print()
    
    # Summary
    print("📊 Run Summary")
    print("=" * 20)
    print(f"Total projects: {len(projects)}")
    print(f"✅ Successful runs: {len(successful_projects)}")
    print(f"❌ Failed runs: {len(failed_projects)}")
    print()
    
    if successful_projects:
        print("🎉 Successfully ran projects:")
        for project in successful_projects:
            print(f"  ✅ {project}")
        print()
    
    if failed_projects:
        print("⚠️  Failed to run projects:")
        for project, error in failed_projects:
            print(f"  ❌ {project}: {error}")
        print()
        print("🛠️  Fix the errors in failed projects and run ./tools/run-all.py again")
        print()
        print("💡 Common Python issues:")
        print("  - Import errors (missing dependencies)")
        print("  - Syntax errors")
        print("  - Missing files or permissions")
        print("  - Virtual environment not activated")
    
    if len(failed_projects) == 0:
        print("🎉 All projects ran successfully!")
        print("💡 Usage examples:")
        print("  python projects/01-file-organizer/main.py")
        print("  python projects/02-password-generator/main.py")
        print("  ./tools/install-deps.py  # Install dependencies")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()