#!/bin/bash

# Run All Tests Script
# This script runs all project tests using CTest

echo "🧪 Running all C++ project tests..."
echo "===================================="

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "❌ Error: build/ directory not found. Please run build-all.sh first."
    exit 1
fi

# Check if projects directory exists
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
    exit 1
fi

cd build

# Discover and show available projects
echo "🔍 Discovering available projects..."
project_count=0
for project_path in ../projects/*/; do
    if [ -d "$project_path" ] && [ -f "${project_path}CMakeLists.txt" ]; then
        project_dir=$(basename "$project_path")
        target_name=$(echo "$project_dir" | sed 's/^[0-9][0-9]*-//')
        echo "  📦 $project_dir → $target_name"
        project_count=$((project_count + 1))
    fi
done

if [ $project_count -eq 0 ]; then
    echo "❌ No projects found!"
    exit 1
fi

echo "📋 Found $project_count projects"
echo ""
echo "🏃 Running all tests..."

# Check if we're using a multi-config generator (like Visual Studio on Windows)
if grep -q "Visual Studio\|Xcode\|Multi-Config" CMakeCache.txt 2>/dev/null; then
    echo "📋 Detected multi-config generator, using Debug configuration..."
    ctest --output-on-failure --verbose -C Debug
else
    echo "📋 Detected single-config generator..."
    ctest --output-on-failure --verbose
fi

echo ""
echo "✅ All tests completed!"
echo "📊 Check above for individual test results"