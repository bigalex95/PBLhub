#pragma once

#include "screen_recorder.h"
#include "recorder_gui.h"
#include <memory>

/**
 * RecorderApplication coordinates between GUI and recording components
 * Implements the main application logic and manages component interactions
 */
class RecorderApplication
{
private:
    std::unique_ptr<ScreenRecorder> recorder;
    std::unique_ptr<RecorderGUI> gui;

    bool is_initialized;
    bool gstreamer_initialized;

    // Event handlers that connect GUI events to recorder actions
    bool on_start_recording(const std::string &filename, int bitrate);
    void on_stop_recording();

    // Status update handlers from recorder to GUI
    void on_recorder_error(const std::string &error_message);
    void on_recorder_state_changed(ScreenRecorder::State new_state);

public:
    RecorderApplication();
    ~RecorderApplication();

    // Application lifecycle
    bool initialize();
    int run(int argc, char *argv[]);
    void shutdown();

    // Static helper for GStreamer/GTK initialization
    static bool check_dependencies();
};