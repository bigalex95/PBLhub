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