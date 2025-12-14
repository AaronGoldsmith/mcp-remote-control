import httpx
import os

# Constants for ECP
ECP_PORT = 8060
TV_IP = os.getenv("HOST_IP")

async def send_ecp_post(command: str) -> bool:
    """Sends a POST request for ECP commands that require an action (e.g., keypress)."""
    
    # ECP commands are sent to port 8060
    url = f"http://{TV_IP}:{ECP_PORT}/{command}" 
    
    # The ECP protocol requires a POST request, often with an empty body
    # We use httpx.AsyncClient for asynchronous requests
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # We send a POST request with an empty body, similar to 'curl -d ""'
            response = await client.post(url, data="") 
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status() 
            return True
            
    except httpx.HTTPError as e:
        return False
    except Exception as e:
        return False
    


# For debugging
async def get_device_info() -> str:
    """Retrieves basic device information (model, software version, etc.) as XML."""
    url = f"http://{TV_IP}:{ECP_PORT}/query/device-info"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url) 
            response.raise_for_status() 
            
            # Returns the raw XML data
            return response.text 
            
    except httpx.HTTPError as e:
        return f"Error retrieving device info from {TV_IP}: {e}. Ensure 'Control by mobile apps' is enabled."
    except Exception as e:
        return f"General Error: {e}"
