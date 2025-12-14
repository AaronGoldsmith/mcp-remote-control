import os
import httpx
from mcp.server.fastmcp import FastMCP

from mcp_remote_control.roku_bridge import send_ecp_post, get_device_info as fetch_device_info

mcp = FastMCP("tv_control",
               instructions="Tools for controlling a Roku TV via ECP commands over the local network.")

# Constants for ECP
ECP_PORT = 8060

# App name to ID mapping
APP_MAPPING = {
    "netflix": "12",
    "youtube": "837",
    "amazon prime video": "13",
    "prime video": "13",
    "hulu": "2285",
    "disney+": "291097",
    "disney plus": "291097",
    "hbo max": "61322",
    "apple tv+": "551012",
    "apple tv": "551012",
    "peacock": "593099",
    "paramount plus": "31440",
    "paramount+": "31440",
    "espn": "34376",
    "tubi": "41468",
    "sling tv": "46041",
    "starz": "65067",
    "cbs": "619667",
    "cnn": "65978",
    "pluto tv": "74519",
    "showtime": "8838",
}

# --- Tool 1: Simulate Keypress ---

@mcp.tool()
async def press_key(key_name: str) -> str:
    """Simulates a single button press on the TV remote.
    
    Args:
        key_name: The name of the key to press (e.g., Home, Select, VolumeUp). 
                  Common keys are Home, Back, Select, Up, Down, Left, Right.
                  Special keys are: PowerOn, PowerOff, VolumeUp, VolumeDown, VolumeMute
    """
    
    # ECP command structure for keypress: keypress/<KEY>
    command = f"keypress/{key_name.title()}" 
    
    success = await send_ecp_post(command)
    
    if success:
        return f"Successfully sent '{key_name.title()}' keypress command to TV."
    else:
        return f"Failed to send '{key_name.title()}' keypress. Check the IP, device status, and if the key name is valid."


# --- Tool 2: Launch Application ---

@mcp.tool()
async def launch_app(app_name: str) -> str:
    """Launches an application on the TV using its name.

    Args:
        app_name: The name of the app to launch (e.g., Netflix, YouTube, Hulu).
                  Case-insensitive. Use list_apps() to see available apps.
    """

    # Normalize the app name to lowercase for lookup
    normalized_name = app_name.lower().strip()

    # Look up the app ID from the mapping
    app_id = APP_MAPPING.get(normalized_name)

    if not app_id:
        available_apps = ", ".join(sorted(set(APP_MAPPING.keys())))
        return f"App '{app_name}' not found in the app mapping. Available apps: {available_apps}. Use list_apps() for the full list."

    # ECP command structure for launch: launch/<channelId>
    command = f"launch/{app_id}"

    success = await send_ecp_post(command)

    if success:
        return f"Successfully launched {app_name} (ID: {app_id}) on TV."
    else:
        return f"Failed to launch {app_name} (ID: {app_id}). Ensure the TV is ready and the app is installed."

# --- Tool 3: List Available Apps ---

@mcp.tool()
async def list_apps() -> str:
    """Lists all available apps and their corresponding Roku channel IDs.

    Returns a formatted list of app names and their IDs that can be used with launch_app().
    """

    # Create a unique mapping (some apps have multiple names pointing to same ID)
    unique_apps = {}
    for name, app_id in APP_MAPPING.items():
        if app_id not in unique_apps:
            unique_apps[app_id] = []
        unique_apps[app_id].append(name)

    # Format the output
    result = "Available Roku Apps:\n\n"
    for app_id in sorted(unique_apps.keys(), key=lambda x: int(x)):
        names = unique_apps[app_id]
        primary_name = names[0].title()
        if len(names) > 1:
            aliases = ", ".join([n.title() for n in names[1:]])
            result += f"- {primary_name} (ID: {app_id}) [also: {aliases}]\n"
        else:
            result += f"- {primary_name} (ID: {app_id})\n"

    result += "\nYou can use any of these names (case-insensitive) with launch_app()."
    return result

# --- Tool 4: Get Device Info ---

@mcp.tool()
async def get_device_info() -> str:
    """Retrieves basic device information (model, software version, etc.) as XML."""
    return await fetch_device_info()

@mcp.tool()
async def power_on() -> str:
    """Powers on the TV."""
    # ECP command structure for power on: keypress/PowerOn
    command = "keypress/PowerOn"
    
    success = await send_ecp_post(command)
    
    if success:
        return f"Successfully sent power on command to TV."
    else:
        return f"Failed to send power on command to TV. Check the IP and device status."


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()