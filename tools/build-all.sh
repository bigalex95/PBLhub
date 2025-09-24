#!/bin/bash

# Build All C++ Projects Script
# This script builds all projects individually and continues on errors

echo "🔧 Building all C++ projects..."
echo "================================"

# Check if we're in the cpp branch
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the cpp branch root."
    exit 1
fi

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

# List of all projects
projects=(
    "01-hello-cmake:hello-cmake"
    "02-calculator-cli:calculator-cli" 
    "03-file-manager:file-manager"
    "04-todo-app:todo-app"
    "05-memory-game:memory-game"
    "06-text-editor:text-editor"
    "07-http-client:http-client"
    "08-thread-pool:thread-pool"
    "09-mini-database:mini-database"
    "10-game-engine:game-engine"
)

echo "🔨 Building projects individually..."
echo ""

# Build each project separately
for project in "${projects[@]}"; do
    IFS=':' read -r project_dir target_name <<< "$project"
    
    echo "🚀 Building $project_dir..."
    
    if cmake --build . --target "$target_name" 2>&1; then
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
    echo "  ./build/projects/01-hello-cmake/hello-cmake"
    echo "  ./build/projects/02-calculator-cli/calculator-cli"
    echo "  ./tools/run-tests.sh  # Run all tests"
    exit 0
else
    exit 1
fi
