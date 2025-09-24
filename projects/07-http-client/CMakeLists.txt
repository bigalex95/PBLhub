cmake_minimum_required(VERSION 3.16)
project(http-client)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(http-client main.cpp)

# Add test
enable_testing()
add_test(NAME http-client-test COMMAND http-client)
