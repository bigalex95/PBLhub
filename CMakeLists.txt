cmake_minimum_required(VERSION 3.16)
project(PBLhub_CPP_Projects)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable testing
enable_testing()

# Function to automatically discover and add all project subdirectories
function(discover_and_add_projects)
    file(GLOB PROJECT_DIRS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "projects/*")
    
    set(PROJECT_TARGETS "")
    
    foreach(PROJECT_DIR ${PROJECT_DIRS})
        if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_DIR})
            # Check if CMakeLists.txt exists in the project directory
            if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_DIR}/CMakeLists.txt)
                message(STATUS "Adding project: ${PROJECT_DIR}")
                add_subdirectory(${PROJECT_DIR})
                
                # Extract target name from project directory name
                # Remove the number prefix (e.g., "01-hello-cmake" -> "hello-cmake")
                string(REGEX REPLACE "^[0-9]+-" "" TARGET_NAME ${PROJECT_DIR})
                string(REPLACE "projects/" "" TARGET_NAME ${TARGET_NAME})
                list(APPEND PROJECT_TARGETS ${TARGET_NAME})
            endif()
        endif()
    endforeach()
    
    # Create a custom target to build all discovered projects
    if(PROJECT_TARGETS)
        add_custom_target(build-all DEPENDS ${PROJECT_TARGETS})
        message(STATUS "Created build-all target with dependencies: ${PROJECT_TARGETS}")
    endif()
endfunction()

# Discover and add all projects
discover_and_add_projects()
