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
Once connected, you can ask Claude:

"Show me all F1 sessions from 2024"

"Get the race session details for Monaco 2023"

"Who drove in session 9158?" (using a session_key)

"Show me all Ferrari drivers from the 2024 Monza race"

<br>

The server handles the API calls to OpenF1 and returns formatted data that Claude can interpret and present to you
