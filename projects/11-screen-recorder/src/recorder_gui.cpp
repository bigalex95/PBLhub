#include "recorder_gui.h"
#include <sstream>
#include <iomanip>
#include <ctime>

RecorderGUI::RecorderGUI()
    : window(nullptr), is_recording(false), timer_id(0)
{
}

RecorderGUI::~RecorderGUI()
{
    if (timer_id > 0)
    {
        g_source_remove(timer_id);
    }
}

bool RecorderGUI::create_interface()
{
    // Create main window
    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Screen Recorder");
    gtk_window_set_default_size(GTK_WINDOW(window), 450, 350);
    gtk_window_set_resizable(GTK_WINDOW(window), FALSE);
    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
    g_signal_connect(window, "destroy", G_CALLBACK(on_window_destroy), this);

    // Create main vertical box
    main_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 15);
    gtk_widget_set_margin_left(main_box, 25);
    gtk_widget_set_margin_right(main_box, 25);
    gtk_widget_set_margin_top(main_box, 25);
    gtk_widget_set_margin_bottom(main_box, 25);
    gtk_container_add(GTK_CONTAINER(window), main_box);

    // Create sections
    create_title_section();
    create_settings_section();
    create_controls_section();
    create_status_section();

    return true;
}

void RecorderGUI::create_title_section()
{
    GtkWidget *title_label = gtk_label_new(nullptr);
    gtk_label_set_markup(GTK_LABEL(title_label),
                         "<span size='large' weight='bold'>Screen Recorder</span>");
    gtk_widget_set_halign(title_label, GTK_ALIGN_CENTER);
    gtk_box_pack_start(GTK_BOX(main_box), title_label, FALSE, FALSE, 0);

    // Add separator
    GtkWidget *separator1 = gtk_separator_new(GTK_ORIENTATION_HORIZONTAL);
    gtk_box_pack_start(GTK_BOX(main_box), separator1, FALSE, FALSE, 5);
}

void RecorderGUI::create_settings_section()
{
    // Settings frame
    GtkWidget *settings_frame = gtk_frame_new("Recording Settings");
    GtkWidget *settings_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_margin_left(settings_box, 15);
    gtk_widget_set_margin_right(settings_box, 15);
    gtk_widget_set_margin_top(settings_box, 10);
    gtk_widget_set_margin_bottom(settings_box, 10);
    gtk_container_add(GTK_CONTAINER(settings_frame), settings_box);

    // Filename entry
    GtkWidget *filename_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    GtkWidget *filename_label = gtk_label_new("Output File:");
    gtk_widget_set_size_request(filename_label, 100, -1);
    gtk_widget_set_halign(filename_label, GTK_ALIGN_START);

    filename_entry = gtk_entry_new();
    gtk_entry_set_text(GTK_ENTRY(filename_entry), generate_default_filename().c_str());
    gtk_entry_set_placeholder_text(GTK_ENTRY(filename_entry), "Enter filename...");

    gtk_box_pack_start(GTK_BOX(filename_box), filename_label, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(filename_box), filename_entry, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(settings_box), filename_box, FALSE, FALSE, 0);

    // Bitrate setting
    GtkWidget *bitrate_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    GtkWidget *bitrate_label = gtk_label_new("Bitrate (kbps):");
    gtk_widget_set_size_request(bitrate_label, 100, -1);
    gtk_widget_set_halign(bitrate_label, GTK_ALIGN_START);

    bitrate_spin = gtk_spin_button_new_with_range(500, 10000, 100);
    gtk_spin_button_set_value(GTK_SPIN_BUTTON(bitrate_spin), 2000);
    gtk_widget_set_tooltip_text(bitrate_spin, "Higher bitrate = better quality, larger file size");

    gtk_box_pack_start(GTK_BOX(bitrate_box), bitrate_label, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(bitrate_box), bitrate_spin, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(settings_box), bitrate_box, FALSE, FALSE, 0);

    gtk_box_pack_start(GTK_BOX(main_box), settings_frame, FALSE, FALSE, 0);
}

void RecorderGUI::create_controls_section()
{
    // Control buttons frame
    GtkWidget *controls_frame = gtk_frame_new("Controls");
    GtkWidget *controls_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_margin_left(controls_box, 15);
    gtk_widget_set_margin_right(controls_box, 15);
    gtk_widget_set_margin_top(controls_box, 10);
    gtk_widget_set_margin_bottom(controls_box, 10);
    gtk_container_add(GTK_CONTAINER(controls_frame), controls_box);

    // Button box
    GtkWidget *button_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 15);
    gtk_widget_set_halign(button_box, GTK_ALIGN_CENTER);

    start_button = gtk_button_new_with_label("Start Recording");
    stop_button = gtk_button_new_with_label("Stop Recording");

    // Style buttons
    gtk_widget_set_size_request(start_button, 140, 40);
    gtk_widget_set_size_request(stop_button, 140, 40);
    gtk_widget_set_sensitive(stop_button, FALSE);

    g_signal_connect(start_button, "clicked", G_CALLBACK(on_start_clicked), this);
    g_signal_connect(stop_button, "clicked", G_CALLBACK(on_stop_clicked), this);

    gtk_box_pack_start(GTK_BOX(button_box), start_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(button_box), stop_button, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(controls_box), button_box, FALSE, FALSE, 0);

    // Timer display
    time_label = gtk_label_new("Ready to record");
    gtk_widget_set_halign(time_label, GTK_ALIGN_CENTER);
    GtkWidget *time_style = time_label;
    gtk_widget_set_name(time_style, "timer-label");
    gtk_box_pack_start(GTK_BOX(controls_box), time_label, FALSE, FALSE, 5);

    gtk_box_pack_start(GTK_BOX(main_box), controls_frame, FALSE, FALSE, 0);
}

void RecorderGUI::create_status_section()
{
    // Status section
    GtkWidget *status_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);

    // Progress bar (hidden initially)
    progress_bar = gtk_progress_bar_new();
    gtk_progress_bar_set_show_text(GTK_PROGRESS_BAR(progress_bar), FALSE);
    gtk_widget_set_no_show_all(progress_bar, TRUE); // Hide by default
    gtk_box_pack_start(GTK_BOX(status_box), progress_bar, FALSE, FALSE, 0);

    // Status label
    status_label = gtk_label_new("Ready");
    gtk_widget_set_halign(status_label, GTK_ALIGN_CENTER);
    gtk_box_pack_start(GTK_BOX(status_box), status_label, FALSE, FALSE, 0);

    gtk_box_pack_start(GTK_BOX(main_box), status_box, FALSE, FALSE, 0);
}

void RecorderGUI::show()
{
    gtk_widget_show_all(window);
}

void RecorderGUI::on_start_clicked(GtkWidget *widget, gpointer user_data)
{
    RecorderGUI *gui = static_cast<RecorderGUI *>(user_data);

    std::string filename = gui->get_filename();
    if (filename.empty())
    {
        gui->update_status("Please enter a filename");
        return;
    }

    int bitrate = gui->get_bitrate();

    if (gui->start_callback)
    {
        bool success = gui->start_callback(filename, bitrate);
        if (!success)
        {
            gui->update_status("Failed to start recording");
        }
    }
}

void RecorderGUI::on_stop_clicked(GtkWidget *widget, gpointer user_data)
{
    RecorderGUI *gui = static_cast<RecorderGUI *>(user_data);

    if (gui->stop_callback)
    {
        gui->stop_callback();
    }
}

void RecorderGUI::on_window_destroy(GtkWidget *widget, gpointer user_data)
{
    RecorderGUI *gui = static_cast<RecorderGUI *>(user_data);

    if (gui->is_recording && gui->stop_callback)
    {
        gui->stop_callback();
    }

    gtk_main_quit();
}

gboolean RecorderGUI::update_timer(gpointer user_data)
{
    RecorderGUI *gui = static_cast<RecorderGUI *>(user_data);

    if (!gui->is_recording)
    {
        return G_SOURCE_REMOVE;
    }

    auto now = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(
        now - gui->recording_start_time);

    int hours = duration.count() / 3600;
    int minutes = (duration.count() % 3600) / 60;
    int seconds = duration.count() % 60;

    gchar *time_str = g_strdup_printf("Recording: %02d:%02d:%02d", hours, minutes, seconds);
    gtk_label_set_text(GTK_LABEL(gui->time_label), time_str);
    g_free(time_str);

    return G_SOURCE_CONTINUE;
}

void RecorderGUI::on_recording_started()
{
    is_recording = true;
    recording_start_time = std::chrono::steady_clock::now();

    update_ui_for_recording_state(true);
    update_status("Recording in progress...");

    // Start timer
    timer_id = g_timeout_add(1000, update_timer, this);
}

void RecorderGUI::on_recording_stopped(const std::string &saved_filename)
{
    is_recording = false;

    // Stop timer
    if (timer_id > 0)
    {
        g_source_remove(timer_id);
        timer_id = 0;
    }

    update_ui_for_recording_state(false);
    gtk_label_set_text(GTK_LABEL(time_label), "Recording completed");
    update_status("Saved: " + saved_filename);
}

void RecorderGUI::on_recording_error(const std::string &error_message)
{
    is_recording = false;

    if (timer_id > 0)
    {
        g_source_remove(timer_id);
        timer_id = 0;
    }

    update_ui_for_recording_state(false);
    gtk_label_set_text(GTK_LABEL(time_label), "Recording failed");
    update_status("Error: " + error_message);
}

void RecorderGUI::update_status(const std::string &message)
{
    gtk_label_set_text(GTK_LABEL(status_label), message.c_str());
}

void RecorderGUI::update_ui_for_recording_state(bool recording)
{
    gtk_widget_set_sensitive(start_button, !recording);
    gtk_widget_set_sensitive(stop_button, recording);
    gtk_widget_set_sensitive(filename_entry, !recording);
    gtk_widget_set_sensitive(bitrate_spin, !recording);
}

std::string RecorderGUI::get_filename() const
{
    return gtk_entry_get_text(GTK_ENTRY(filename_entry));
}

int RecorderGUI::get_bitrate() const
{
    return static_cast<int>(gtk_spin_button_get_value(GTK_SPIN_BUTTON(bitrate_spin)));
}

std::string RecorderGUI::generate_default_filename()
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

void RecorderGUI::run()
{
    gtk_main();
}

void RecorderGUI::quit()
{
    gtk_main_quit();
}