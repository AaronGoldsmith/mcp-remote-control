# MCP Remote Control


![MCP Remote Control](cover_image.png)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that enables AI assistants and agentic systems to control TVs on your local network.

**Currently supports:** Roku TVs via the External Control Protocol (ECP).

## What is MCP?

The Model Context Protocol is an open standard that allows AI models to securely interact with external tools and data sources. This server exposes TV controls as MCP tools, enabling LLMs like Claude to control your TV through natural language commands.

## Architecture

This project is designed with future extensibility in mind. The Roku-specific implementation is isolated in `roku_bridge.py`, separating the ECP protocol details from the MCP server layer. While the current implementation is Roku-specific, the structure provides a foundation for supporting additional TV brands and control protocols in the future.

## Why Use This?

- **Natural Language Control**: Tell your AI assistant "turn on Netflix" or "increase the volume" without touching a remote
- **Smart Home Integration**: Integrate TV control into agentic workflows and automation systems
- **Accessibility**: Control your TV through conversational interfaces
- **Development**: Build custom applications that leverage AI-powered TV control

## Prerequisites

### TV Setup

Before using this server, you need to enable external control on your Roku TV:

1. **Enable Network Control**:
   - Go to **Settings** > **System** > **Advanced system settings**
   - Select **Control by mobile apps**
   - Choose **Network access** and set to **Default** or **Permissive**

2. **Find Your TV's IP Address**:
   - Go to **Settings** > **Network** > **About**
   - Note the IP address (e.g., `192.168.1.100`)

3. **Set Environment Variable**:
   ```bash
   export HOST_IP=192.168.1.100  # Replace with your TV's IP
   ```

### System Requirements

- **Python**: 3.12 or higher
- **Network**: TV and computer must be on the same local network
- **MCP Client**: An MCP-compatible client like [Claude Desktop](https://claude.ai/download), [Claude Code](https://github.com/anthropics/claude-code), [Goose](https://block.github.io/goose/docs/getting-started/installation) or custom implementations

## Features

- **Remote Control**: Simulate button presses (navigation, playback, volume, power)
- **App Launching**: Launch apps by name (e.g., "Netflix", "YouTube")
- **App Discovery**: List all available apps and their IDs
- **Device Info**: Query device information


## Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp-remote-control
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   # or with uv:
   uv pip install -e .
   ```

3. **Set your TV's IP address**:
   ```bash
   export HOST_IP=192.168.1.100  # Replace with your actual TV IP
   ```

### Using with Claude Desktop

Add this server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**If you installed with uv (recommended):**

```json
{
  "mcpServers": {
    "tv-control": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-remote-control", "run", "mcp-remote-control"],
      "env": {
        "HOST_IP": "192.168.1.100"
      }
    }
  }
}
```

**If you installed globally (with `pip install -e .` or `uv pip install -e .`):**

```json
{
  "mcpServers": {
    "tv-control": {
      "command": "mcp-remote-control",
      "env": {
        "HOST_IP": "192.168.1.100"
      }
    }
  }
}
```

Replace `/absolute/path/to/mcp-remote-control` with the actual path to your cloned repository, and `192.168.1.100` with your TV's IP address.

After updating the config, restart Claude Desktop. You can then ask Claude to control your TV:
- "Turn on my TV and launch Netflix"
- "Increase the volume"
- "What apps are available on my Roku?"

### Using with Claude Code

Install the server using the MCP server manager in Claude Code. See the [Claude Code documentation](https://github.com/anthropics/claude-code) for details.

### Using with Other MCP Clients

This server uses the standard MCP protocol over stdio. See the [MCP documentation](https://modelcontextprotocol.io/docs/develop/connect-local-servers) for connecting local servers to your MCP client. 


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

## Example Usage

Once connected to an MCP client, you can use natural language to control your TV:

```
User: "Turn on my TV and launch Netflix"
Assistant: *uses power_on() and launch_app("Netflix")*

User: "Show me what apps are available"
Assistant: *uses list_apps() to display all installed apps*

User: "Navigate down 3 times and select"
Assistant: *uses press_key("Down") three times, then press_key("Select")*

User: "Pause what's playing"
Assistant: *uses press_key("Pause")*
```

## Learn More

### MCP Resources

- **[Model Context Protocol Documentation](https://modelcontextprotocol.io)** - Official MCP docs and specification
- **[MCP GitHub Repository](https://github.com/modelcontextprotocol)** - Source code and examples
- **[MCP Servers Registry](https://github.com/modelcontextprotocol/servers)** - Collection of community MCP servers
- **[Building MCP Servers Guide](https://modelcontextprotocol.io/docs/build/servers)** - Learn to build your own MCP servers

### Roku Resources

- **[Roku ECP Documentation](https://developer.roku.com/docs/developer-program/dev-tools/external-control-api.md)** - Official External Control Protocol documentation
- **[Roku Developer Portal](https://developer.roku.com)** - Additional Roku development resources

## Troubleshooting

- **Connection Failed**: Ensure your TV and computer are on the same network and the TV's IP address is correct
- **Control Not Working**: Verify that "Control by mobile apps" is enabled in your TV settings
- **App Not Launching**: Check that the app is installed on your TV using `list_apps()`
- **Environment Variable**: Make sure `HOST_IP` is set in your shell or MCP client configuration

## License

MIT
