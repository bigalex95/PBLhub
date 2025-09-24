cmake_minimum_required(VERSION 3.16)
project(PBLhub_CPP_Projects)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add all project subdirectories
add_subdirectory(projects/01-hello-cmake)
add_subdirectory(projects/02-calculator-cli)
add_subdirectory(projects/03-file-manager)
add_subdirectory(projects/04-todo-app)
add_subdirectory(projects/05-memory-game)
add_subdirectory(projects/06-text-editor)
add_subdirectory(projects/07-http-client)
add_subdirectory(projects/08-thread-pool)
add_subdirectory(projects/09-mini-database)
add_subdirectory(projects/10-game-engine)

# Enable testing
enable_testing()

# Add a custom target to build all projects
add_custom_target(build-all
    DEPENDS
    hello-cmake
    calculator-cli
    file-manager
    todo-app
    memory-game
    text-editor
    http-client
    thread-pool
    mini-database
    game-engine
)
