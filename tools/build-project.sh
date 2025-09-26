#!/bin/bash

# Build Single C++ Project Script
# This script builds a specific project by name or number

# Function to show usage
show_usage() {
    echo "Usage: $0 <project_name_or_number>"
    echo ""
    echo "Examples:"
    echo "  $0 hello-cmake          # Build by target name"
    echo "  $0 01-hello-cmake       # Build by directory name"
    echo "  $0 1                    # Build by project number"
    echo "  $0 calculator-cli       # Build calculator project"
    echo "  $0 02                   # Build project 02"
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
            
            echo "  $project_num. $project_dir → $target_name"
        fi
    done
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

# Parse input argument
input_project="$1"

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
echo ""

# Create build directory
echo "📁 Setting up build directory..."
mkdir -p build
cd build

# Configure CMake if not already configured
if [ ! -f "CMakeCache.txt" ]; then
    echo "📦 Configuring CMake..."
    if ! cmake ..; then
        echo "❌ CMake configuration failed!"
        exit 1
    fi
else
    echo "📦 Using existing CMake configuration..."
fi

echo ""
echo "🔨 Building project: $project_dir"
echo "🎯 Target: $target_name"
echo "================================"

# Build the specific project
# Check if we're using a multi-config generator
if grep -q "Visual Studio\|Xcode\|Multi-Config" CMakeCache.txt 2>/dev/null; then
    build_command="cmake --build . --target $target_name --config Debug"
else
    build_command="cmake --build . --target $target_name"
fi

echo "🚀 Running: $build_command"
echo ""

if $build_command; then
    echo ""
    echo "🎉 Successfully built $project_dir!"
    echo "📁 Executable location: build/projects/$project_dir/$target_name"
    echo ""
    echo "💡 Run it with:"
    echo "  ./build/projects/$project_dir/$target_name"
else
    echo ""
    echo "❌ Build failed for $project_dir"
    echo ""
    echo "🛠️  Common C++ compilation issues to check:"
    echo "  - Missing semicolons (;)"
    echo "  - Undeclared variables or functions"
    echo "  - Missing #include statements"
    echo "  - Syntax errors in $project_dir/main.cpp"
    echo ""
    echo "🔍 Check the error messages above for specific details."
    exit 1
fi

# Return to root directory
cd ..