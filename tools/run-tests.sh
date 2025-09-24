#!/bin/bash

# Run All Tests Script
# This script runs all project tests using CTest

set -e  # Exit on any error

echo "🧪 Running all C++ project tests..."
echo "===================================="

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "❌ Error: build/ directory not found. Please run build-all.sh first."
    exit 1
fi

cd build

echo "🏃 Running all tests..."
ctest --output-on-failure --verbose

echo ""
echo "✅ All tests completed!"
echo "📊 Check above for individual test results"