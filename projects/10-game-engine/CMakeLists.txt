cmake_minimum_required(VERSION 3.16)
project(game-engine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(game-engine main.cpp)

# Add test
enable_testing()
add_test(NAME game-engine-test COMMAND game-engine)
