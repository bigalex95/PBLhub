cmake_minimum_required(VERSION 3.16)
project(text-editor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(text-editor main.cpp)

# Add test
enable_testing()
add_test(NAME text-editor-test COMMAND text-editor)
