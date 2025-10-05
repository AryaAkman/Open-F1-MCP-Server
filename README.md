<p align="center">
    <img src="https://openf1.org/images/logo-5882a735.png" width="150" height="150"/>
</p>

# Open-F1-MCP-Server
This project implements the MCP Server for Open Formula 1 

For more detailed information, please check [Implementation of Open F1 MCP Server](www.aryaakman.com/projects/Open-F1-MCP-Server.html)

<br>


## What is Open Formula 1
[Open Formula 1](www.openf1.org) is an open-source API that provides real-time and historical Formula 1 data.

The API offers a wealth of information, including lap timings, car telemetry, radio communications, and more. Whether you're looking to create interactive dashboards, dive deep into race analysis, or even develop connected objects that light up every time your favorite driver takes the lead, OpenF1 makes it all possible.

<br>

# Open F1 MCP Server Installation instructions for Claude:

## 1. Install dependencies:

bashpip install mcp httpx

<br>

## 2. Add/update Claude desktop config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "Open-F1": {
      "command": "python",
      "args": ["/path/to/OpenF1MCPServer.py"]
    }
  }
}
```
<br>

## 3. Restart Claude desktop and verify the installation
Go to Claude Desktop -> File -> Settings -> Developer

On the right side of the screen, look under Local MCP Servers and verify 
- "Open-F1" shows up
-  The state is "running" (highlighted with blue background)

<br>

## Usage examples
The following example prompts can provide ideas on how to utilize this MCP Server 

- ### Sessions (Race) related usage examples
    - "Show me all F1 sessions from 2024"
    
    - "Get the race session details for Monaco 2023"

- ### Driver related usage examples
    - "Who drove in session 9158?" (using a session_key)

    - "Show me all Ferrari drivers from the 2024 Monza race"

- ### Lap information related usage examples
    - "Get lap 10 data for all drivers in the Monaco 2024 race"

    - "What was Max Verstappen's fastest lap in the last race?"

    - "Compare sector times for lap 1 between drivers 1 and 44 in session 9158"

<br>

The server handles the API calls to OpenF1 and returns formatted data that Claude can interpret and present to you

<br>


## Supported APIs in this version (v1.1):
- get_sessions: Retrieve F1 race sessions with optional filtering
- get_drivers: Retrieve driver information for all drivers or a specific session
- get_laps: Retrieve lap data for specific session/driver/lap combinations
  
