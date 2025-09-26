#!/bin/bash

# Test Single C++ Project Script  
# This script runs tests for a specific project by name or number

# Function to show usage
show_usage() {
    echo "Usage: $0 <project_name_or_number> [ctest_options...]"
    echo ""
    echo "Examples:"
    echo "  $0 hello-cmake              # Test by target name"
    echo "  $0 01-hello-cmake           # Test by directory name"
    echo "  $0 1                        # Test by project number"
    echo "  $0 calculator-cli --verbose # Test with verbose output"
    echo "  $0 02 --output-on-failure   # Test project 02 with failure details"
    echo ""
    echo "Available projects:"
    list_projects
}

# Function to list all available projects with test status
list_projects() {
    if [ ! -d "projects" ]; then
        echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
        return 1
    fi
    
    echo "📋 Available projects:"
    for project_path in projects/*/; do
        if [ -d "$project_path" ] && [ -f "${project_path}CMakeLists.txt" ]; then
            project_dir=$(basename "$project_path")
            # Extract target name from project directory name
            target_name=$(echo "$project_dir" | sed 's/^[0-9][0-9]*-//')
            # Extract number from project directory name
            project_num=$(echo "$project_dir" | grep -o '^[0-9][0-9]*')
            
            # Check if executable exists (needed for testing)
            exe_path="build/projects/$project_dir/$target_name"
            if [ -f "$exe_path" ]; then
                # Check if we're in build directory to use ctest
                if [ -d "build" ] && [ -f "build/CMakeCache.txt" ]; then
                    echo "  $project_num. $project_dir → $target_name ✅ (ready to test)"
                else
                    echo "  $project_num. $project_dir → $target_name ⚠️  (build not configured)"
                fi
            else
                echo "  $project_num. $project_dir → $target_name ❌ (not built)"
            fi
        fi
    done
    echo ""
    echo "Legend:"
    echo "  ✅ Ready to test"
    echo "  ⚠️  Build directory needs configuration (run build-all.sh or build-project.sh)"
    echo "  ❌ Project needs to be built first"
}

# Function to find project by various input formats
find_project() {
    local input="$1"
    
    # Check if input is empty
    if [ -z "$input" ]; then
        return 1
    fi
    
    # Search through all projects
    for project_path in projects/*/; do
        if [ -d "$project_path" ] && [ -f "${project_path}CMakeLists.txt" ]; then
            project_dir=$(basename "$project_path")
            target_name=$(echo "$project_dir" | sed 's/^[0-9][0-9]*-//')
            project_num=$(echo "$project_dir" | grep -o '^[0-9][0-9]*')
            
            # Match by exact project directory name
            if [ "$input" = "$project_dir" ]; then
                echo "$project_dir:$target_name"
                return 0
            fi
            
            # Match by target name
            if [ "$input" = "$target_name" ]; then
                echo "$project_dir:$target_name"
                return 0
            fi
            
            # Match by project number (with or without leading zero)
            if [ "$input" = "$project_num" ] || [ "$input" = "${project_num#0}" ]; then
                echo "$project_dir:$target_name"
                return 0
            fi
        fi
    done
    
    return 1
}

# Function to check if project is ready for testing
check_test_readiness() {
    local project_dir="$1"
    local target_name="$2"
    
    # Check if build directory exists
    if [ ! -d "build" ]; then
        echo "❌ Build directory not found"
        return 1
    fi
    
    # Check if CMakeCache exists
    if [ ! -f "build/CMakeCache.txt" ]; then
        echo "❌ CMake not configured"
        return 2
    fi
    
    # Check if executable exists
    exe_path="build/projects/$project_dir/$target_name"
    if [ ! -f "$exe_path" ]; then
        echo "❌ Executable not found: $exe_path"
        return 3
    fi
    
    return 0
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "❌ Error: No project specified!"
    echo ""
    show_usage
    exit 1
fi

# Check if we're in the correct directory
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
    exit 1
fi

# Parse input arguments
input_project="$1"
shift  # Remove first argument, keep the rest as ctest options

# Handle special cases
if [ "$input_project" = "--help" ] || [ "$input_project" = "-h" ]; then
    show_usage
    exit 0
fi

if [ "$input_project" = "--list" ] || [ "$input_project" = "-l" ]; then
    list_projects
    exit 0
fi

# Find the project
echo "🔍 Looking for project: $input_project"
project_info=$(find_project "$input_project")

if [ -z "$project_info" ]; then
    echo "❌ Project '$input_project' not found!"
    echo ""
    echo "💡 Try one of these:"
    list_projects
    exit 1
fi

# Parse project info
IFS=':' read -r project_dir target_name <<< "$project_info"

echo "✅ Found project: $project_dir → $target_name"

# Check if project is ready for testing
readiness_check=$(check_test_readiness "$project_dir" "$target_name")
readiness_code=$?

if [ $readiness_code -ne 0 ]; then
    echo "$readiness_check"
    echo ""
    case $readiness_code in
        1)
            echo "🔨 Build the project first:"
            echo "   ./tools/build-project.sh $input_project"
            echo ""
            echo "🔧 Or build all projects:"
            echo "   ./tools/build-all.sh"
            ;;
        2)
            echo "📦 Configure CMake first:"
            echo "   ./tools/build-project.sh $input_project"
            echo ""
            echo "🔧 Or configure for all projects:"
            echo "   ./tools/build-all.sh"
            ;;
        3)
            echo "🔨 Build the executable first:"
            echo "   ./tools/build-project.sh $input_project"
            ;;
    esac
    exit 1
fi

# Change to build directory
cd build

# Prepare test name (matches the pattern in CMakeLists.txt)
test_name="${target_name}-test"

echo "🧪 Test name: $test_name"

# Prepare ctest command with options
ctest_options="--output-on-failure"
if [ $# -gt 0 ]; then
    echo "🎯 Additional CTest options: $*"
    ctest_options="$ctest_options $*"
fi

# Check if we're using a multi-config generator
if grep -q "Visual Studio\|Xcode\|Multi-Config" CMakeCache.txt 2>/dev/null; then
    ctest_command="ctest -R $test_name $ctest_options -C Debug"
else
    ctest_command="ctest -R $test_name $ctest_options"
fi

echo ""
echo "🚀 Running: $ctest_command"
echo "================================"

# Run the specific test
if $ctest_command; then
    exit_code=$?
    echo ""
    echo "✅ Test for $project_dir passed successfully!"
else
    exit_code=$?
    echo ""
    echo "❌ Test for $project_dir failed!"
    echo ""
    echo "🛠️  Possible issues:"
    echo "  - Program returned non-zero exit code"
    echo "  - Runtime error in the executable"
    echo "  - Program crashed or threw exception"
    echo ""
    echo "💡 Debug suggestions:"
    echo "   # Run the executable directly to see output:"
    echo "   ./tools/run-project.sh $input_project"
    echo ""
    echo "   # Run with verbose test output:"
    echo "   ./tools/test-project.sh $input_project --verbose"
    exit $exit_code
fi

# Return to root directory
cd ..