cmake_minimum_required(VERSION 3.16)
project(file-manager)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(file-manager main.cpp)

# Add test
enable_testing()
add_test(NAME file-manager-test COMMAND file-manager)
