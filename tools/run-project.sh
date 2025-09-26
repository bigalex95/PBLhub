#!/bin/bash

# Run Single C++ Project Script
# This script runs a specific project by name or number

# Function to show usage
show_usage() {
    echo "Usage: $0 <project_name_or_number> [arguments...]"
    echo ""
    echo "Examples:"
    echo "  $0 hello-cmake              # Run by target name"
    echo "  $0 01-hello-cmake           # Run by directory name"
    echo "  $0 1                        # Run by project number"
    echo "  $0 calculator-cli 5 + 3     # Run with arguments"
    echo "  $0 02 --help                # Run project 02 with --help"
    echo ""
    echo "Available projects:"
    list_projects
}

# Function to list all available projects
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
            
            # Check if executable exists
            exe_path="build/projects/$project_dir/$target_name"
            if [ -f "$exe_path" ]; then
                echo "  $project_num. $project_dir → $target_name ✅"
            else
                echo "  $project_num. $project_dir → $target_name ⚠️  (not built)"
            fi
        fi
    done
    echo ""
    echo "⚠️  Projects marked with ⚠️  need to be built first:"
    echo "   ./tools/build-project.sh <project_name>"
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

# Function to check if executable exists
check_executable() {
    local project_dir="$1"
    local target_name="$2"
    local exe_path="build/projects/$project_dir/$target_name"
    
    if [ -f "$exe_path" ]; then
        return 0
    else
        return 1
    fi
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
shift  # Remove first argument, keep the rest as program arguments

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

# Check if executable exists
exe_path="build/projects/$project_dir/$target_name"
if ! check_executable "$project_dir" "$target_name"; then
    echo "❌ Executable not found: $exe_path"
    echo ""
    echo "🔨 Build the project first:"
    echo "   ./tools/build-project.sh $input_project"
    echo ""
    echo "🔧 Or build all projects:"
    echo "   ./tools/build-all.sh"
    exit 1
fi

echo "📁 Executable: $exe_path"

# Prepare command with arguments
if [ $# -gt 0 ]; then
    echo "🎯 Arguments: $*"
    run_command="./$exe_path $*"
else
    run_command="./$exe_path"
fi

echo ""
echo "🚀 Running: $run_command"
echo "================================"

# Run the project with arguments
if $run_command; then
    exit_code=$?
    echo ""
    echo "✅ Project $project_dir completed successfully (exit code: $exit_code)"
else
    exit_code=$?
    echo ""
    echo "❌ Project $project_dir failed (exit code: $exit_code)"
    echo ""
    echo "🛠️  Possible issues:"
    echo "  - Runtime error in the program"
    echo "  - Invalid arguments provided"
    echo "  - Missing dependencies or resources"
    echo ""
    echo "💡 Try running without arguments or check the project's documentation:"
    echo "   ./tools/run-project.sh $input_project"
    exit $exit_code
fi