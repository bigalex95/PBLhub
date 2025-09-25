#!/bin/bash

# Build All C++ Projects Script
# This script dynamically discovers and builds all projects individually

echo "🔧 Building all C++ projects..."
echo "================================"

# Check if we're in the cpp branch
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
    exit 1
fi

# Function to discover all projects dynamically
discover_projects() {
    # Find all directories in projects/ that contain CMakeLists.txt
    for project_path in ../projects/*/; do
        if [ -d "$project_path" ] && [ -f "${project_path}CMakeLists.txt" ]; then
            project_dir=$(basename "$project_path")
            
            # Extract target name from project directory name
            # Remove the number prefix (e.g., "01-hello-cmake" -> "hello-cmake")
            target_name=$(echo "$project_dir" | sed 's/^[0-9][0-9]*-//')
            
            echo "$project_dir:$target_name"
        fi
    done
}

# Create build directory
mkdir -p build
cd build

# Configure CMake
echo "📦 Configuring CMake..."
if ! cmake ..; then
    echo "❌ CMake configuration failed!"
    exit 1
fi

# Arrays to track build results
declare -a successful_projects=()
declare -a failed_projects=()

# Dynamically discover all projects
echo "🔍 Discovering projects..."
readarray -t projects < <(discover_projects)

if [ ${#projects[@]} -eq 0 ]; then
    echo "❌ No projects found in projects/ directory!"
    exit 1
fi

echo "📋 Found ${#projects[@]} projects:"
for project in "${projects[@]}"; do
    IFS=':' read -r project_dir target_name <<< "$project"
    echo "  - $project_dir → $target_name"
done
echo ""

echo "🔨 Building projects individually..."
echo ""

# Build each project separately
for project in "${projects[@]}"; do
    IFS=':' read -r project_dir target_name <<< "$project"
    
    echo "🚀 Building $project_dir..."
    
    # Check if we're using a multi-config generator (like Visual Studio on Windows)
    if grep -q "Visual Studio\|Xcode\|Multi-Config" CMakeCache.txt 2>/dev/null; then
        build_result=$(cmake --build . --target "$target_name" --config Debug 2>&1)
    else
        build_result=$(cmake --build . --target "$target_name" 2>&1)
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ $project_dir built successfully"
        successful_projects+=("$project_dir")
    else
        echo "❌ $project_dir failed to build"
        failed_projects+=("$project_dir")
    fi
    echo ""
done

# Return to root directory
cd ..

echo "📊 Build Summary"
echo "================"
echo "Total projects: ${#projects[@]}"
echo "✅ Successful builds: ${#successful_projects[@]}"
echo "❌ Failed builds: ${#failed_projects[@]}"
echo ""

if [ ${#successful_projects[@]} -gt 0 ]; then
    echo "🎉 Successfully built projects:"
    for project in "${successful_projects[@]}"; do
        echo "  ✅ $project"
    done
    echo ""
fi

if [ ${#failed_projects[@]} -gt 0 ]; then
    echo "⚠️  Failed to build projects:"
    for project in "${failed_projects[@]}"; do
        echo "  ❌ $project"
    done
    echo ""
    echo "🛠️  Fix the errors in failed projects and run ./tools/build-all.sh again"
    echo ""
    echo "💡 Common C++ compilation issues:"
    echo "  - Missing semicolons (;)"
    echo "  - Undeclared variables or functions" 
    echo "  - Missing #include statements"
    echo "  - Syntax errors"
fi

if [ ${#failed_projects[@]} -eq 0 ]; then
    echo "🎉 All projects built successfully!"
    echo "📁 Executables location: build/projects/*/[project-name]"
    echo ""
    echo "💡 Usage examples:"
    
    # Show examples for first few successful projects
    count=0
    for project in "${successful_projects[@]}"; do
        if [ $count -lt 3 ]; then
            # Find the original project directory name for this target
            for proj_entry in "${projects[@]}"; do
                IFS=':' read -r proj_dir target_name <<< "$proj_entry"
                if [ "$project" = "$proj_dir" ]; then
                    echo "  ./build/projects/$proj_dir/$target_name"
                    break
                fi
            done
            ((count++))
        else
            break
        fi
    done
    
    echo "  ./tools/run-tests.sh  # Run all tests"
    exit 0
else
    exit 1
fi
