## GUI Screenshots

The Screen Recorder features a clean, intuitive GTK3 interface:

### Main Window

```
┌─────────────────────────────────────┐
│           Screen Recorder           │
├─────────────────────────────────────┤
│                                     │
│        Screen Recorder              │
│                                     │
│ Filename: [screen_recording_...]    │
│ Bitrate (kbps): [2000    ▲▼]       │
│                                     │
│   [Start Recording] [Stop Recording] │
│                                     │
│         Ready to record             │
│              Ready                  │
└─────────────────────────────────────┘
```

### During Recording

```
┌─────────────────────────────────────┐
│           Screen Recorder           │
├─────────────────────────────────────┤
│                                     │
│        Screen Recorder              │
│                                     │
│ Filename: [my_recording.mp4    ]    │
│ Bitrate (kbps): [2000    ▲▼]       │
│                                     │
│   [      ] [Stop Recording]         │
│                                     │
│      Recording: 00:01:23            │
│    Recording started successfully   │
└─────────────────────────────────────┘
```

## Interface Elements

- **Filename Field**: Custom filename or auto-generated timestamp
- **Bitrate Spinner**: Adjustable from 500-10000 kbps
- **Start Button**: Begin screen recording (disabled during recording)
- **Stop Button**: End recording gracefully (enabled during recording)
- **Timer Display**: Live recording duration in HH:MM:SS format
- **Status Label**: Current application status and feedback
