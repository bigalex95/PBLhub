#!/bin/bash

# Build All C++ Projects Script
# This script builds all projects in the projects/ directory

set -e  # Exit on any error

echo "🔧 Building all C++ projects..."
echo "================================"

# Check if we're in the cpp branch
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
    exit 1
fi

# Counter for tracking builds
total_projects=0
successful_builds=0
failed_builds=0

# Build each project
for project_dir in projects/*/; do
    if [ -d "$project_dir" ]; then
        project_name=$(basename "$project_dir")
        echo ""
        echo "🚀 Building project: $project_name"
        echo "-----------------------------------"
        
        total_projects=$((total_projects + 1))
        
        # Check if CMakeLists.txt exists
        if [ -f "$project_dir/CMakeLists.txt" ]; then
            cd "$project_dir"
            
            # Create build directory if it doesn't exist
            mkdir -p build
            cd build
            
            # Build the project
            if cmake .. && make; then
                echo "✅ Successfully built $project_name"
                successful_builds=$((successful_builds + 1))
            else
                echo "❌ Failed to build $project_name"
                failed_builds=$((failed_builds + 1))
            fi
            
            # Return to cpp branch root
            cd ../../..
        else
            echo "⚠️  No CMakeLists.txt found in $project_name, skipping..."
        fi
    fi
done

echo ""
echo "📊 Build Summary"
echo "================"
echo "Total projects: $total_projects"
echo "Successful builds: $successful_builds"
echo "Failed builds: $failed_builds"

if [ $failed_builds -eq 0 ]; then
    echo "🎉 All projects built successfully!"
    exit 0
else
    echo "⚠️  Some projects failed to build. Check the output above for details."
    exit 1
fi
