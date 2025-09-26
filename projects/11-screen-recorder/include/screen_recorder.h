#pragma once

#include <string>
#include <functional>
#include <chrono>
#include <gst/gst.h>

/**
 * ScreenRecorder handles the GStreamer pipeline for screen recording
 * Separated from GUI logic for better modularity
 */
class ScreenRecorder
{
public:
    struct Settings
    {
        std::string output_filename;
        int bitrate = 2000; // kbps
        bool show_cursor = true;

        Settings() = default;
        Settings(const std::string &filename, int bitrate_kbps = 2000, bool cursor = true)
            : output_filename(filename), bitrate(bitrate_kbps), show_cursor(cursor) {}
    };

    enum class State
    {
        IDLE,
        INITIALIZING,
        RECORDING,
        STOPPING,
        ERROR
    };

    // Callback types for status updates
    using ErrorCallback = std::function<void(const std::string &error_message)>;
    using StateCallback = std::function<void(State new_state)>;

private:
    GstElement *pipeline;
    GstElement *source;
    GstElement *videoconvert;
    GstElement *encoder;
    GstElement *muxer;
    GstElement *filesink;

    State current_state;
    Settings current_settings;
    std::chrono::steady_clock::time_point recording_start_time;

    ErrorCallback error_callback;
    StateCallback state_callback;

    // GStreamer message bus callback
    static gboolean bus_callback(GstBus *bus, GstMessage *message, gpointer user_data);

    void set_state(State new_state);
    void cleanup_pipeline();

public:
    ScreenRecorder();
    ~ScreenRecorder();

    // Configuration
    void set_error_callback(ErrorCallback callback) { error_callback = callback; }
    void set_state_callback(StateCallback callback) { state_callback = callback; }

    // Core functionality
    bool initialize(const Settings &settings);
    bool start_recording();
    void stop_recording();

    // Status
    State get_state() const { return current_state; }
    std::chrono::duration<double> get_recording_duration() const;
    const Settings &get_settings() const { return current_settings; }

    // Utility
    static std::string generate_filename();
    static bool check_gstreamer_elements();
};