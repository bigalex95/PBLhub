cmake_minimum_required(VERSION 3.16)
project(screen-recorder)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(screen-recorder main.cpp)

# Add test
enable_testing()
add_test(NAME screen-recorder-test COMMAND screen-recorder)
