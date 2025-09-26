#pragma once

#include <gtk/gtk.h>
#include <string>
#include <functional>
#include <chrono>

/**
 * RecorderGUI handles the GTK interface for the screen recorder
 * Separated from recording logic for better modularity
 */
class RecorderGUI
{
public:
    // Callback types for GUI events
    using StartRecordingCallback = std::function<bool(const std::string &filename, int bitrate)>;
    using StopRecordingCallback = std::function<void()>;

private:
    // GTK widgets
    GtkWidget *window;
    GtkWidget *main_box;
    GtkWidget *start_button;
    GtkWidget *stop_button;
    GtkWidget *status_label;
    GtkWidget *filename_entry;
    GtkWidget *bitrate_spin;
    GtkWidget *time_label;
    GtkWidget *progress_bar;

    // State
    bool is_recording;
    std::chrono::steady_clock::time_point recording_start_time;
    guint timer_id;

    // Callbacks
    StartRecordingCallback start_callback;
    StopRecordingCallback stop_callback;

    // Internal widget creation methods
    void create_title_section();
    void create_settings_section();
    void create_controls_section();
    void create_status_section();

    // Event handlers
    static void on_start_clicked(GtkWidget *widget, gpointer user_data);
    static void on_stop_clicked(GtkWidget *widget, gpointer user_data);
    static void on_window_destroy(GtkWidget *widget, gpointer user_data);

    // Timer callback for updating recording duration
    static gboolean update_timer(gpointer user_data);

    void update_ui_for_recording_state(bool recording);
    std::string generate_default_filename();

public:
    RecorderGUI();
    ~RecorderGUI();

    // Setup and initialization
    bool create_interface();
    void show();

    // Callback registration
    void set_start_recording_callback(StartRecordingCallback callback) { start_callback = callback; }
    void set_stop_recording_callback(StopRecordingCallback callback) { stop_callback = callback; }

    // Status updates from recorder
    void on_recording_started();
    void on_recording_stopped(const std::string &saved_filename);
    void on_recording_error(const std::string &error_message);
    void update_status(const std::string &message);

    // State management
    bool get_is_recording() const { return is_recording; }
    std::string get_filename() const;
    int get_bitrate() const;

    // Main loop control
    void run();
    void quit();
};