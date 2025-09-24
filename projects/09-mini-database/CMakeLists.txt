cmake_minimum_required(VERSION 3.16)
project(mini-database)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mini-database main.cpp)

# Add test
enable_testing()
add_test(NAME mini-database-test COMMAND mini-database)
