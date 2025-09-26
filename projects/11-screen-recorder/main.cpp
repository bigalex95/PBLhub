#include "recorder_application.h"
#include <iostream>

/**
 * Main entry point for the Screen Recorder application
 * This file demonstrates the clean separation of concerns in the new architecture
 */
int main(int argc, char *argv[])
{
    // Create and run the application
    // Dependencies will be checked after GStreamer initialization
    RecorderApplication app;
    return app.run(argc, argv);
}