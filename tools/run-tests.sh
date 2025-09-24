#!/bin/bash

# Run All Python Tests Script
# This script runs tests for all projects in the projects/ directory

set -e  # Exit on any error

echo "🧪 Running all Python project tests..."
echo "====================================="

# Check if we're in the python branch
if [ ! -d "projects" ]; then
    echo "❌ Error: projects/ directory not found. Make sure you're in the python branch root."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Consider running ./tools/setup-env.sh first."
fi

# Counter for tracking tests
total_projects=0
successful_tests=0
failed_tests=0
no_tests=0

# Run tests for each project
for project_dir in projects/*/; do
    if [ -d "$project_dir" ]; then
        project_name=$(basename "$project_dir")
        echo ""
        echo "🧪 Testing project: $project_name"
        echo "--------------------------------"
        
        total_projects=$((total_projects + 1))
        
        cd "$project_dir"
        
        # Check if tests directory or test files exist
        if [ -d "tests" ] || ls test_*.py 1> /dev/null 2>&1 || ls *_test.py 1> /dev/null 2>&1; then
            # Install project-specific requirements if they exist
            if [ -f "requirements.txt" ]; then
                echo "📦 Installing project dependencies..."
                pip install -r requirements.txt
            fi
            
            # Run pytest
            if pytest -v; then
                echo "✅ Tests passed for $project_name"
                successful_tests=$((successful_tests + 1))
            else
                echo "❌ Tests failed for $project_name"
                failed_tests=$((failed_tests + 1))
            fi
        else
            echo "⚠️  No tests found for $project_name"
            no_tests=$((no_tests + 1))
        fi
        
        # Return to python branch root
        cd ../..
    fi
done

echo ""
echo "📊 Test Summary"
echo "==============="
echo "Total projects: $total_projects"
echo "Successful tests: $successful_tests"
echo "Failed tests: $failed_tests"
echo "No tests found: $no_tests"

if [ $failed_tests -eq 0 ]; then
    echo "🎉 All available tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed. Check the output above for details."
    exit 1
fi
