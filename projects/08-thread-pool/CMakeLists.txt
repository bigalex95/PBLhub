cmake_minimum_required(VERSION 3.16)
project(thread-pool)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(thread-pool main.cpp)

# Add test
enable_testing()
add_test(NAME thread-pool-test COMMAND thread-pool)
