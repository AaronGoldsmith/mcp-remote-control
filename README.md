# MCP Remote Control

Use ECP commands to control Roku TVs on your local network.

## Features

- **Remote Control**: Simulate button presses (navigation, playback, volume, power)
- **App Launching**: Launch apps by name (e.g., "Netflix", "YouTube")
- **App Discovery**: List all available apps and their IDs
- **Device Info**: Query device information

## Available Tools

### `press_key(key_name)`
Simulates a button press on the TV remote.
- **Navigation**: Home, Up, Down, Left, Right, Select, Back
- **Playback**: Play, Pause, Rev (Rewind), Fwd (FastForward)
- **Volume**: VolumeUp, VolumeDown, VolumeMute
- **Power**: PowerOff, PowerOn
- **Other**: Info, InstantReplay, Search

### `launch_app(app_name)`
Launches an app by name (case-insensitive). Examples:
- `launch_app("Netflix")`
- `launch_app("youtube")`
- `launch_app("Disney+")`

### `list_apps()`
Lists all available apps with their names and Roku channel IDs.

### `get_device_info()`
Retrieves device information as XML.

### `power_on()`
Powers on the TV.

## Supported Apps

The following apps are supported and can be launched by name using `launch_app()`. App names are case-insensitive and some apps have multiple accepted names (e.g., "Prime Video" or "Amazon Prime Video").

| App Name | Channel ID | Alternative Names |
|----------|------------|-------------------|
| Netflix | 12 | - |
| YouTube | 837 | - |
| Amazon Prime Video | 13 | Prime Video |
| Hulu | 2285 | - |
| Disney+ | 291097 | Disney Plus |
| HBO Max | 61322 | - |
| Apple TV+ | 551012 | Apple TV |
| Peacock | 593099 | - |
| Paramount Plus | 31440 | Paramount+ |
| ESPN | 34376 | - |
| Tubi | 41468 | - |
| Sling TV | 46041 | - |
| STARZ | 65067 | - |
| CBS | 619667 | - |
| CNN | 65978 | - |
| Pluto TV | 74519 | - |
| SHOWTIME | 8838 | - |

Use `list_apps()` to see the complete list programmatically.
