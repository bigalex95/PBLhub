# Screen Recorder - Modular Architecture

## Project Structure

The screen recorder has been refactored into a clean, modular architecture with clear separation of concerns:

```
11-screen-recorder/
├── include/                    # Header files
│   ├── screen_recorder.h       # Core recording functionality
│   ├── recorder_gui.h          # GTK user interface
│   └── recorder_application.h  # Application coordinator
├── src/                        # Implementation files
│   ├── screen_recorder.cpp     # GStreamer pipeline management
│   ├── recorder_gui.cpp        # GTK interface implementation
│   └── recorder_application.cpp# Application logic & coordination
├── main.cpp                    # Simple entry point
├── CMakeLists.txt             # Build configuration
└── README.md                  # Usage documentation
```

## Components Overview

### 1. ScreenRecorder Class (`screen_recorder.h/.cpp`)

**Responsibility:** Pure GStreamer pipeline management and screen recording functionality

**Key Features:**

- GStreamer pipeline creation and management
- Recording state management (IDLE, RECORDING, STOPPING, ERROR)
- Configurable recording settings (bitrate, filename, cursor visibility)
- Asynchronous callbacks for status updates
- Error handling and resource cleanup

**Interface:**

```cpp
class ScreenRecorder {
public:
    struct Settings { /* recording configuration */ };
    enum class State { IDLE, INITIALIZING, RECORDING, STOPPING, ERROR };

    bool initialize(const Settings& settings);
    bool start_recording();
    void stop_recording();
    State get_state() const;
    // ... callback setters and utilities
};
```

### 2. RecorderGUI Class (`recorder_gui.h/.cpp`)

**Responsibility:** Pure GTK3 user interface without any recording logic

**Key Features:**

- Clean GTK3 interface with organized sections
- Recording controls (start/stop buttons)
- Settings configuration (filename, bitrate)
- Real-time recording timer display
- Status feedback and progress indication
- Callback-based communication with application logic

**Interface:**

```cpp
class RecorderGUI {
public:
    using StartRecordingCallback = std::function<bool(const std::string&, int)>;
    using StopRecordingCallback = std::function<void()>;

    bool create_interface();
    void show();
    void run();

    // Status updates from external components
    void on_recording_started();
    void on_recording_stopped(const std::string& filename);
    void on_recording_error(const std::string& error);
};
```

### 3. RecorderApplication Class (`recorder_application.h/.cpp`)

**Responsibility:** Coordination and application logic - the "glue" between GUI and recorder

**Key Features:**

- Manages lifecycle of GUI and recorder components
- Translates GUI events to recorder actions
- Handles status updates between components
- Dependency checking and initialization
- Resource management and cleanup

**Interface:**

```cpp
class RecorderApplication {
public:
    bool initialize();
    int run(int argc, char* argv[]);
    void shutdown();

    static bool check_dependencies();
};
```

### 4. Main Entry Point (`main.cpp`)

**Responsibility:** Minimal entry point that creates and runs the application

**Features:**

- Dependency checking before startup
- Simple application creation and execution
- Clean error handling

## Architecture Benefits

### ✅ **Separation of Concerns**

- **GUI logic** separated from **recording logic**
- **Application coordination** separated from component implementation
- Each class has a single, well-defined responsibility

### ✅ **Testability**

- Each component can be tested independently
- Mock implementations can easily replace real components
- Clear interfaces make unit testing straightforward

### ✅ **Maintainability**

- Changes to GUI don't affect recording logic and vice versa
- Easy to add new features to specific components
- Clear code organization makes debugging easier

### ✅ **Extensibility**

- Easy to add new recording formats or sources
- GUI can be replaced with different toolkit (Qt, etc.)
- New features can be added without touching existing code

### ✅ **Reusability**

- ScreenRecorder can be used in different applications
- GUI components can be reused for similar applications
- Clean interfaces enable code reuse

## Communication Flow

```
User Input (GUI) → RecorderApplication → ScreenRecorder → GStreamer Pipeline
                       ↓                      ↓
Status Updates (GUI) ← RecorderApplication ← ScreenRecorder ← GStreamer Messages
```

1. **User clicks "Start"** → GUI calls application callback
2. **Application** creates recording settings and calls recorder
3. **Recorder** initializes GStreamer pipeline and starts recording
4. **Status updates** flow back through callbacks to update GUI
5. **User clicks "Stop"** → Same flow but for stopping

## Build System

The CMakeLists.txt now properly handles:

- Multiple source files compilation
- Header include directories
- Library linking for all components
- Clean dependency management

## Development Workflow

To add new features:

1. **New recording feature** → Modify `ScreenRecorder` class
2. **New UI element** → Modify `RecorderGUI` class
3. **New application logic** → Modify `RecorderApplication` class
4. **Integration** → Update callbacks and communication flow

This architecture provides a solid foundation for future enhancements while keeping the codebase clean, maintainable, and professional.
