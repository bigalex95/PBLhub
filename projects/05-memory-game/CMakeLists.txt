cmake_minimum_required(VERSION 3.16)
project(memory-game)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(memory-game main.cpp)

# Add test
enable_testing()
add_test(NAME memory-game-test COMMAND memory-game)
