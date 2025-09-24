cmake_minimum_required(VERSION 3.16)
project(calculator-cli)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(calculator-cli main.cpp)

# Add test
enable_testing()
add_test(NAME calculator-cli-test COMMAND calculator-cli)
