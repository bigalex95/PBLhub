#!/usr/bin/env python3
"""
Setup Verification Script
Verifies that all virtual environment tools are working correctly
"""

import subprocess
import sys
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


def test_script_execution():
    """Test that all scripts can be executed"""
    scripts = [
        ("setup-venv.py", "Virtual Environment Setup"),
        ("setup-uv.py", "UV Package Manager Setup"),
        ("env-manager.py", "Environment Manager"),
        ("install-deps.py", "Dependency Installer"),
        ("run-all.py", "Project Runner"),
    ]

    print("🧪 Testing Script Execution")
    print("=" * 30)

    all_passed = True

    for script_name, description in scripts:
        script_path = Path("tools") / script_name

        if not script_path.exists():
            print(f"❌ {description}: Script not found")
            all_passed = False
            continue

        # Test help/usage output
        success, stdout, stderr = run_command(f"python3 {script_path}")

        if success or "Usage:" in stderr or "Usage:" in stdout:
            print(f"✅ {description}: Can execute")
        else:
            print(f"❌ {description}: Execution failed")
            print(f"   Error: {stderr}")
            all_passed = False

    return all_passed


def test_python_sh():
    """Test the python.sh wrapper script"""
    print("\n🧪 Testing Python.sh Wrapper")
    print("=" * 30)

    script_path = Path("tools/python.sh")

    if not script_path.exists():
        print("❌ python.sh not found")
        return False

    success, stdout, stderr = run_command("bash tools/python.sh")

    if "Usage:" in stdout or "Usage:" in stderr:
        print("✅ python.sh: Shows usage correctly")
        return True
    else:
        print("❌ python.sh: Does not show usage")
        print(f"   Output: {stdout}")
        print(f"   Error: {stderr}")
        return False


def test_directory_structure():
    """Test that the directory structure is correct"""
    print("\n🧪 Testing Directory Structure")
    print("=" * 30)

    required_dirs = ["projects", "tools", "resources"]

    required_files = [
        "BUILD_SETUP.md",
        "README.md",
        "tools/setup-venv.py",
        "tools/setup-uv.py",
        "tools/env-manager.py",
        "tools/install-deps.py",
        "tools/run-all.py",
        "tools/python.sh",
    ]

    all_passed = True

    # Check directories
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory: {dir_name}")
        else:
            print(f"❌ Directory missing: {dir_name}")
            all_passed = False

    # Check files
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ File: {file_name}")
        else:
            print(f"❌ File missing: {file_name}")
            all_passed = False

    return all_passed


def test_projects_structure():
    """Test that all projects have the required files"""
    print("\n🧪 Testing Project Structure")
    print("=" * 30)

    # Get projects dynamically
    get_project_names, _ = get_projects_config()
    projects = get_project_names()

    if not projects:
        print("❌ No projects found!")
        return False

    all_passed = True

    for project_name in projects:
        project_path = Path("projects") / project_name
        main_file = project_path / "main.py"
        req_file = project_path / "requirements.txt"

        if not project_path.exists():
            print(f"❌ {project_name}: Project directory missing")
            all_passed = False
            continue

        if main_file.exists():
            print(f"✅ {project_name}: main.py exists")
        else:
            print(f"❌ {project_name}: main.py missing")
            all_passed = False

        if req_file.exists():
            print(f"✅ {project_name}: requirements.txt exists")
        else:
            print(f"⚠️  {project_name}: requirements.txt missing")

    return all_passed


def main():
    print("🔍 PBLhub Virtual Environment Setup Verification")
    print("=" * 50)

    all_tests_passed = True

    # Run all tests
    tests = [
        test_directory_structure,
        test_projects_structure,
        test_script_execution,
        test_python_sh,
    ]

    for test_func in tests:
        if not test_func():
            all_tests_passed = False

    # Summary
    print("\n" + "=" * 50)
    print("📊 Verification Summary")
    print("=" * 50)

    if all_tests_passed:
        print("🎉 All tests PASSED! Setup is ready to use.")
        print("\n💡 Next steps:")
        print("1. Setup virtual environment:")
        print("   python tools/setup-venv.py setup-global")
        print("2. Check environment status:")
        print("   python tools/env-manager.py status")
        print("3. Install dependencies:")
        print("   python tools/install-deps.py")
        print("4. Run projects:")
        print("   python tools/run-all.py")

        print("\n🔧 Alternative setups:")
        print("• UV package manager: python tools/setup-uv.py setup-all")
        print("• Individual venvs:   python tools/setup-venv.py setup-individual")
        print("• Quick wrapper:      ./tools/python.sh setup-venv")

    else:
        print("❌ Some tests FAILED. Please check the errors above.")
        print("\n🛠️  Common fixes:")
        print("• Make sure you're in the PBLhub root directory")
        print("• Check that all files were created correctly")
        print("• Verify Python 3.6+ is installed")

    sys.exit(0 if all_tests_passed else 1)


if __name__ == "__main__":
    main()
