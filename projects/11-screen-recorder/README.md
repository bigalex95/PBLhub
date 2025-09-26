# Screen Recorder with GUI

## Overview

This is a modern screen recorder with a GTK3 graphical user interface that captures your full desktop screen and saves it as an MP4 video file using GStreamer.

## Features

- ✅ **Modern GTK3 GUI** - User-friendly graphical interface
- ✅ **Full screen recording** - Captures entire desktop
- ✅ **H.264 video encoding** (x264) - High quality compression
- ✅ **MP4 output format** - Universal video format
- ✅ **Mouse cursor capture** - Includes cursor in recordings
- ✅ **Configurable bitrate** - Adjust quality/file size (500-10000 kbps)
- ✅ **Custom filename** - Set your own output filename
- ✅ **Real-time timer** - See recording duration live
- ✅ **Status feedback** - Visual feedback on recording status

## Project Architecture

This screen recorder uses a **modular architecture** with clear separation of concerns:

- **`ScreenRecorder`** - Pure GStreamer recording functionality
- **`RecorderGUI`** - GTK3 user interface components
- **`RecorderApplication`** - Application logic and coordination
- **`main.cpp`** - Simple entry point

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## How to Build

```bash
cd /home/bigalex95/Projects/Pet_Projects/PBLhub/projects/11-screen-recorder
cmake -B build .
cmake --build build
```

Or use the project tools:

```bash
cd /home/bigalex95/Projects/Pet_Projects/PBLhub
./tools/build-project.sh 11
./tools/run-project.sh 11
```

## How to Use

### GUI Interface

1. **Launch the application:**

   ```bash
   ./build/projects/11-screen-recorder/screen-recorder
   ```

2. **Configure recording:**

   - **Filename:** Enter your desired output filename (auto-generates with timestamp)
   - **Bitrate:** Adjust video quality (500-10000 kbps, default 2000)

3. **Start/Stop Recording:**

   - Click **Start Recording** to begin
   - Click **Stop Recording** to end
   - Real-time timer shows recording duration
   - Status bar shows current state

4. **Output:** Video file is automatically saved to the specified location

## Output

- **File Format:** MP4
- **Video Codec:** H.264 (x264)
- **Bitrate:** 2 Mbps
- **Filename:** `screen_recording_YYYYMMDD_HHMMSS.mp4`
- **Location:** Current working directory

## Example Output

```
=== Screen Recorder ===
Starting screen recording...
Output file: screen_recording_20250926_190822.mp4
Recording started. Press Ctrl+C to stop.
Pipeline state changed from NULL to READY
Pipeline state changed from READY to PAUSED
Pipeline state changed from PAUSED to PLAYING

^C
Received signal 2

Stopping recording...
Recording stopped. Video saved to: screen_recording_20250926_190822.mp4
```

## Troubleshooting

- **No video created:** Ensure you have X11 display server running
- **Permission denied:** Make sure you have access to the display
- **Poor quality:** Adjust bitrate in the source code (encoder bitrate property)
- **Large file size:** Lower the bitrate or resolution in the code

## Technical Details

- Uses `ximagesrc` for X11 screen capture
- Pipeline: `ximagesrc -> videoconvert -> x264enc -> mp4mux -> filesink`
- Handles graceful shutdown with EOS (End of Stream) events
- Real-time encoding with medium quality preset
