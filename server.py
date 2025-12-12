from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging to stderr to avoid corrupting JSON-RPC messages
# This is a crucial best practice for STDIO-based servers
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', filename='/dev/stderr')

# Initialize FastMCP server with a descriptive name
mcp = FastMCP("tv_control")

# Constants for ECP
ECP_PORT = 8060

async def send_ecp_post(tv_ip: str, command: str) -> bool:
    """Sends a POST request for ECP commands that require an action (e.g., keypress)."""
    
    # ECP commands are sent to port 8060
    url = f"http://{tv_ip}:{ECP_PORT}/{command}" 
    
    # The ECP protocol requires a POST request, often with an empty body
    # We use httpx.AsyncClient for asynchronous requests
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # We send a POST request with an empty body, similar to 'curl -d ""'
            response = await client.post(url, data="") 
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status() 
            logging.info(f"Successfully sent ECP command: {command}")
            return True
            
    except httpx.HTTPError as e:
        return False
    except Exception as e:
        return False
    
# --- Tool 1: Simulate Keypress ---

@mcp.tool()
async def press_key(tv_ip: str, key_name: str) -> str:
    """Simulates a single button press on the TV remote.
    
    Args:
        tv_ip: The IP address of the TV (e.g., 192.168.1.100).
        key_name: The name of the key to press (e.g., Home, Select, VolumeUp). 
                  Common keys are Home, Back, Select, Up, Down, Left, Right.
    """
    
    # ECP command structure for keypress: keypress/<KEY>
    command = f"keypress/{key_name.title()}" 
    
    success = await send_ecp_post(tv_ip, command)
    
    if success:
        return f"Successfully sent '{key_name.title()}' keypress command to TV at {tv_ip}."
    else:
        return f"Failed to send '{key_name.title()}' keypress. Check the IP, device status, and if the key name is valid."


# --- Tool 2: Launch Application ---

@mcp.tool()
async def launch_app(tv_ip: str, app_id: str) -> str:
    """Launches an application on the TV using its channel ID.
    
    Args:
        tv_ip: The IP address of the TV.
        app_id: The Channel ID of the app (e.g., 12 for Netflix).
    """
    
    # ECP command structure for launch: launch/<channelId>
    command = f"launch/{app_id}"
    
    success = await send_ecp_post(tv_ip, command)
    
    if success:
        return f"Successfully sent launch command for app ID {app_id} to TV at {tv_ip}."
    else:
        return f"Failed to launch app ID {app_id}. Ensure the app ID is correct and the TV is ready."

# --- Tool 3: Get Device Info (Example of a GET request) ---

@mcp.tool()
async def get_device_info(tv_ip: str) -> str:
    """Retrieves basic device information (model, software version, etc.) as XML.
    
    Args:
        tv_ip: The IP address of the TV.
    """
    url = f"http://{tv_ip}:{ECP_PORT}/query/device-info"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url) 
            response.raise_for_status() 
            
            # Returns the raw XML data
            return response.text 
            
    except httpx.HTTPError as e:
        return f"Error retrieving device info from {tv_ip}: {e}. Ensure 'Control by mobile apps' is enabled."
    except Exception as e:
        return f"General Error: {e}"
    


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()