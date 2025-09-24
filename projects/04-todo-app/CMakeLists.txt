cmake_minimum_required(VERSION 3.16)
project(todo-app)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(todo-app main.cpp)

# Add test
enable_testing()
add_test(NAME todo-app-test COMMAND todo-app)
