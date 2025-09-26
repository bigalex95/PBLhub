#include "screen_recorder.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#include <ctime>

ScreenRecorder::ScreenRecorder()
    : pipeline(nullptr), source(nullptr), videoconvert(nullptr),
      encoder(nullptr), muxer(nullptr), filesink(nullptr),
      current_state(State::IDLE)
{
}

ScreenRecorder::~ScreenRecorder()
{
    cleanup_pipeline();
}

bool ScreenRecorder::initialize(const Settings &settings)
{
    if (current_state != State::IDLE)
    {
        return false;
    }

    set_state(State::INITIALIZING);
    current_settings = settings;

    // Create pipeline
    pipeline = gst_pipeline_new("screen-recorder-pipeline");
    if (!pipeline)
    {
        if (error_callback)
        {
            error_callback("Failed to create GStreamer pipeline");
        }
        set_state(State::ERROR);
        return false;
    }

    // Create elements
    source = gst_element_factory_make("ximagesrc", "screen-source");
    videoconvert = gst_element_factory_make("videoconvert", "video-convert");
    encoder = gst_element_factory_make("x264enc", "video-encoder");
    muxer = gst_element_factory_make("mp4mux", "muxer");
    filesink = gst_element_factory_make("filesink", "file-sink");

    if (!source || !videoconvert || !encoder || !muxer || !filesink)
    {
        if (error_callback)
        {
            error_callback("Failed to create required GStreamer elements. Please check your GStreamer installation.");
        }
        cleanup_pipeline();
        set_state(State::ERROR);
        return false;
    }

    // Configure elements
    g_object_set(source,
                 "use-damage", FALSE,
                 "show-pointer", settings.show_cursor ? TRUE : FALSE,
                 NULL);

    g_object_set(encoder,
                 "bitrate", settings.bitrate,
                 "speed-preset", 2,  // Medium preset
                 "tune", 0x00000004, // Zero latency
                 NULL);

    g_object_set(filesink, "location", settings.output_filename.c_str(), NULL);

    // Add elements to pipeline
    gst_bin_add_many(GST_BIN(pipeline), source, videoconvert, encoder, muxer, filesink, NULL);

    // Link elements
    if (!gst_element_link_many(source, videoconvert, encoder, muxer, filesink, NULL))
    {
        if (error_callback)
        {
            error_callback("Failed to link pipeline elements");
        }
        cleanup_pipeline();
        set_state(State::ERROR);
        return false;
    }

    // Set up message bus
    GstBus *bus = gst_element_get_bus(pipeline);
    gst_bus_add_watch(bus, bus_callback, this);
    gst_object_unref(bus);

    set_state(State::IDLE);
    return true;
}

bool ScreenRecorder::start_recording()
{
    if (current_state != State::IDLE || !pipeline)
    {
        return false;
    }

    GstStateChangeReturn ret = gst_element_set_state(pipeline, GST_STATE_PLAYING);
    if (ret == GST_STATE_CHANGE_FAILURE)
    {
        if (error_callback)
        {
            error_callback("Failed to start recording pipeline");
        }
        set_state(State::ERROR);
        return false;
    }

    recording_start_time = std::chrono::steady_clock::now();
    set_state(State::RECORDING);
    return true;
}

void ScreenRecorder::stop_recording()
{
    if (current_state != State::RECORDING || !pipeline)
    {
        return;
    }

    set_state(State::STOPPING);

    // Send EOS event to properly close the file
    gst_element_send_event(pipeline, gst_event_new_eos());

    // The actual stopping will happen in the bus callback when EOS is received
}

std::chrono::duration<double> ScreenRecorder::get_recording_duration() const
{
    if (current_state != State::RECORDING)
    {
        return std::chrono::duration<double>::zero();
    }

    auto now = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::duration<double>>(now - recording_start_time);
}

std::string ScreenRecorder::generate_filename()
{
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    auto tm = *std::localtime(&time_t);

    std::ostringstream oss;
    oss << "screen_recording_"
        << std::put_time(&tm, "%Y%m%d_%H%M%S")
        << ".mp4";

    return oss.str();
}

bool ScreenRecorder::check_gstreamer_elements()
{
    const char *required_elements[] = {
        "ximagesrc", "videoconvert", "x264enc", "mp4mux", "filesink"};

    for (const char *element_name : required_elements)
    {
        GstElementFactory *factory = gst_element_factory_find(element_name);
        if (!factory)
        {
            return false;
        }
        gst_object_unref(factory);
    }

    return true;
}

gboolean ScreenRecorder::bus_callback(GstBus *bus, GstMessage *message, gpointer user_data)
{
    ScreenRecorder *recorder = static_cast<ScreenRecorder *>(user_data);

    switch (GST_MESSAGE_TYPE(message))
    {
    case GST_MESSAGE_ERROR:
    {
        gchar *debug;
        GError *error;
        gst_message_parse_error(message, &error, &debug);

        std::string error_msg = "GStreamer Error: " + std::string(error->message);
        if (recorder->error_callback)
        {
            recorder->error_callback(error_msg);
        }

        if (debug)
            g_free(debug);
        g_error_free(error);

        recorder->set_state(State::ERROR);
        break;
    }
    case GST_MESSAGE_EOS:
        // End of stream reached, recording finished
        gst_element_set_state(recorder->pipeline, GST_STATE_NULL);
        recorder->set_state(State::IDLE);
        break;
    case GST_MESSAGE_STATE_CHANGED:
    {
        GstState old_state, new_state, pending_state;
        gst_message_parse_state_changed(message, &old_state, &new_state, &pending_state);

        // Only handle pipeline state changes
        if (GST_OBJECT(message->src) == GST_OBJECT(recorder->pipeline))
        {
            // Additional state handling can be added here if needed
        }
        break;
    }
    default:
        break;
    }

    return TRUE;
}

void ScreenRecorder::set_state(State new_state)
{
    if (current_state != new_state)
    {
        current_state = new_state;
        if (state_callback)
        {
            state_callback(new_state);
        }
    }
}

void ScreenRecorder::cleanup_pipeline()
{
    if (pipeline)
    {
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(pipeline);
        pipeline = nullptr;
    }

    // Reset element pointers (they're owned by the pipeline)
    source = videoconvert = encoder = muxer = filesink = nullptr;
}