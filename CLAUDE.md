# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that enables AI assistants to control Roku TVs on the local network using the External Control Protocol (ECP). The server exposes TV control functions as MCP tools that can be called by LLMs through natural language.

**Architecture:** The project is structured with the Roku-specific ECP protocol implementation isolated in `roku_bridge.py`, separate from the MCP server layer in `server.py`. While the current implementation is tightly coupled to Roku (ECP commands, key names, channel IDs), this separation provides a foundation for future extensibility to other TV brands and control protocols.

## Development Setup

### Installation
```bash
# Install dependencies
pip install -e .
# or with uv:
uv pip install -e .
```

### Environment Configuration
The server requires the `HOST_IP` environment variable to be set to the Roku TV's IP address:
```bash
export HOST_IP=192.168.1.100  # Replace with actual TV IP
```

### Running the Server
```bash
# Run the MCP server (uses stdio transport)
python server.py
```

The server runs as an MCP server using stdio transport, designed to be launched by MCP clients like Claude Desktop or Claude Code.

## Architecture

### Core Components

**server.py** - Main MCP server implementation using FastMCP
- Defines all MCP tools that AI assistants can invoke
- Contains app name-to-ID mapping for popular streaming services
- Orchestrates calls to roku_bridge for actual ECP communication
- Entry point: `main()` function that starts the MCP server with stdio transport

**roku_bridge.py** - Low-level ECP communication layer
- `send_ecp_post(command)`: Sends POST requests to TV's ECP endpoint (port 8060)
- `get_device_info()`: Queries TV device information via GET request
- Uses `httpx.AsyncClient` for all HTTP communication (5 second timeout)
- Reads `HOST_IP` from environment variable

**main.py** - Simple placeholder/test entry point (not used in production)

### MCP Tools Exposed

The server exposes these tools to AI assistants:
- `press_key(key_name)` - Simulate remote button presses (navigation, volume, power, etc.)
- `launch_app(app_name)` - Launch apps by name (case-insensitive, uses APP_MAPPING)
- `list_apps()` - Display all available apps with their channel IDs
- `get_device_info()` - Retrieve device info XML
- `power_on()` - Convenience function to power on the TV

### Roku ECP Protocol

All commands are sent to `http://{TV_IP}:8060/` endpoints:
- Keypresses: `POST /keypress/{KeyName}` with empty body
- App launch: `POST /launch/{channelId}` with empty body
- Device info: `GET /query/device-info`

Key names use title case (e.g., `PowerOn`, `VolumeUp`, `Select`).

### App Mapping

The `APP_MAPPING` dictionary in server.py maps user-friendly app names to Roku channel IDs. Multiple names can map to the same ID (e.g., "amazon prime video" and "prime video" both map to ID "13"). When adding new apps, ensure names are lowercase in the mapping.

## Key Dependencies

- **mcp[cli]** (>=1.23.3) - Model Context Protocol server framework (FastMCP)
- **httpx** (>=0.28.1) - Async HTTP client for ECP requests
- **Python 3.12+** - Required minimum version

## Common Modifications

### Adding New Apps
Add entries to the `APP_MAPPING` dictionary in server.py (line 14-36):
```python
"app name": "channel_id",  # Use lowercase for app name
```

### Adding New Remote Keys
The ECP protocol supports many keys. Just use the correct key name with `press_key()`. Common keys: Home, Back, Select, Up, Down, Left, Right, Play, Pause, Fwd, Rev, VolumeUp, VolumeDown, VolumeMute, PowerOn, PowerOff, Info, InstantReplay, Search.

### Adjusting Timeout
HTTP timeout is set to 5 seconds in roku_bridge.py (lines 17, 38). Modify the `timeout` parameter in `httpx.AsyncClient()` if needed.

## Troubleshooting

### Connection Issues
- Verify `HOST_IP` environment variable is set correctly
- Ensure TV and computer are on the same local network
- Check that "Control by mobile apps" is enabled in TV settings (Settings > System > Advanced system settings > Control by mobile apps > Network access)

### Tool Behavior
- All tools return string messages indicating success/failure
- Failed requests return False from `send_ecp_post()` and result in error messages
- App not found errors include list of available apps in the response
