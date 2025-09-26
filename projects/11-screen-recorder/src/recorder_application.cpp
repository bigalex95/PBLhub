#include "recorder_application.h"
#include <iostream>

RecorderApplication::RecorderApplication()
    : recorder(std::make_unique<ScreenRecorder>()),
      gui(std::make_unique<RecorderGUI>()),
      is_initialized(false), gstreamer_initialized(false)
{
}

RecorderApplication::~RecorderApplication()
{
    shutdown();
}

bool RecorderApplication::initialize()
{
    if (is_initialized)
    {
        return true;
    }

    // Create GUI
    if (!gui->create_interface())
    {
        std::cerr << "Error: Failed to create GUI interface\n";
        return false;
    }

    // Set up callbacks between GUI and recorder
    gui->set_start_recording_callback(
        [this](const std::string &filename, int bitrate)
        {
            return this->on_start_recording(filename, bitrate);
        });

    gui->set_stop_recording_callback(
        [this]()
        {
            this->on_stop_recording();
        });

    // Set up recorder callbacks
    recorder->set_error_callback(
        [this](const std::string &error)
        {
            this->on_recorder_error(error);
        });

    recorder->set_state_callback(
        [this](ScreenRecorder::State state)
        {
            this->on_recorder_state_changed(state);
        });

    is_initialized = true;
    return true;
}

int RecorderApplication::run(int argc, char *argv[])
{
    // Initialize GTK and GStreamer
    gtk_init(&argc, &argv);
    gst_init(&argc, &argv);
    gstreamer_initialized = true;

    // Check GStreamer dependencies after initialization
    if (!ScreenRecorder::check_gstreamer_elements())
    {
        std::cerr << "Error: Required GStreamer elements are not available.\n"
                  << "Please install the following GStreamer plugins:\n"
                  << "- gstreamer1.0-plugins-good (for ximagesrc)\n"
                  << "- gstreamer1.0-plugins-ugly (for x264enc)\n"
                  << "- gstreamer1.0-plugins-bad (for mp4mux)\n";
        gst_deinit();
        return 1;
    }

    if (!initialize())
    {
        gst_deinit();
        return 1;
    }

    std::cout << "Screen Recorder started successfully\n";

    // Show GUI and run main loop
    gui->show();
    gui->run();

    // Cleanup
    shutdown();
    return 0;
}

void RecorderApplication::shutdown()
{
    if (recorder && recorder->get_state() == ScreenRecorder::State::RECORDING)
    {
        recorder->stop_recording();
    }

    if (gstreamer_initialized)
    {
        gst_deinit();
        gstreamer_initialized = false;
    }
    is_initialized = false;
}

bool RecorderApplication::on_start_recording(const std::string &filename, int bitrate)
{
    if (!recorder || recorder->get_state() != ScreenRecorder::State::IDLE)
    {
        return false;
    }

    // Create recorder settings
    ScreenRecorder::Settings settings(filename, bitrate, true);

    // Initialize and start recording
    if (!recorder->initialize(settings))
    {
        return false;
    }

    if (!recorder->start_recording())
    {
        return false;
    }

    // Notify GUI
    gui->on_recording_started();
    std::cout << "Recording started: " << filename << " (bitrate: " << bitrate << " kbps)\n";

    return true;
}

void RecorderApplication::on_stop_recording()
{
    if (recorder && recorder->get_state() == ScreenRecorder::State::RECORDING)
    {
        recorder->stop_recording();
        std::cout << "Stopping recording...\n";
    }
}

void RecorderApplication::on_recorder_error(const std::string &error_message)
{
    std::cerr << "Recorder error: " << error_message << std::endl;
    gui->on_recording_error(error_message);
}

void RecorderApplication::on_recorder_state_changed(ScreenRecorder::State new_state)
{
    switch (new_state)
    {
    case ScreenRecorder::State::IDLE:
        if (gui->get_is_recording())
        {
            // Recording just finished
            std::string filename = recorder->get_settings().output_filename;
            gui->on_recording_stopped(filename);
            std::cout << "Recording completed: " << filename << std::endl;
        }
        break;

    case ScreenRecorder::State::ERROR:
        gui->on_recording_error("Recording failed");
        break;

    default:
        break;
    }
}

bool RecorderApplication::check_dependencies()
{
    // This function should be called after GStreamer is already initialized
    // We'll check dependencies in the run() method after initialization
    return true;
}