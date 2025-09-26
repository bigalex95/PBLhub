cmake_minimum_required(VERSION 3.16)
project(screen-recorder)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(PkgConfig REQUIRED)

# Find GStreamer libraries
pkg_check_modules(GSTREAMER REQUIRED gstreamer-1.0)
pkg_check_modules(GSTREAMER_APP REQUIRED gstreamer-app-1.0)
pkg_check_modules(GSTREAMER_VIDEO REQUIRED gstreamer-video-1.0)

# Find GTK3 for GUI
pkg_check_modules(GTK3 REQUIRED gtk+-3.0)

# Include directories
include_directories(${GSTREAMER_INCLUDE_DIRS})
include_directories(${GSTREAMER_APP_INCLUDE_DIRS})
include_directories(${GSTREAMER_VIDEO_INCLUDE_DIRS})
include_directories(${GTK3_INCLUDE_DIRS})

# Add compile definitions
add_definitions(${GSTREAMER_CFLAGS_OTHER})
add_definitions(${GTK3_CFLAGS_OTHER})

# Include directories for headers
include_directories(include)

# Source files
set(SOURCES
    src/screen_recorder.cpp
    src/recorder_gui.cpp
    src/recorder_application.cpp
    main.cpp
)

add_executable(screen-recorder ${SOURCES})

# Link GStreamer and GTK libraries
target_link_libraries(screen-recorder
    ${GSTREAMER_LIBRARIES}
    ${GSTREAMER_APP_LIBRARIES}
    ${GSTREAMER_VIDEO_LIBRARIES}
    ${GTK3_LIBRARIES}
)

# Add library directories
link_directories(${GSTREAMER_LIBRARY_DIRS})
link_directories(${GSTREAMER_APP_LIBRARY_DIRS})
link_directories(${GSTREAMER_VIDEO_LIBRARY_DIRS})
link_directories(${GTK3_LIBRARY_DIRS})

# Add test
enable_testing()
add_test(NAME screen-recorder-test COMMAND screen-recorder)
