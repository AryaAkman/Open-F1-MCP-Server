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

# Tools (as of v1.2)

### get_sessions:
Retrieve F1 race sessions. Can filter by year, country, circuit, session type, etc. Returns session details including session_key, date, location, and type.

    Parameter	        Description
    year		        Filter by year (e.g., 2023, 2024).
    country_name	    Filter by country name (e.g., 'Monaco', 'Italy').
    circuit_short_name	Filter by circuit short name (e.g., 'Monza', 'Monaco').
    session_name    	Filter by session name (e.g., 'Race', 'Qualifying', 'Sprint').
    session_key	    	Get specific session by its unique session_key.
    date_start	    	Filter by start date (ISO format: YYYY-MM-DD). Supports filters like >= and <=.
    Other filters		session_type, location, country_code, meeting_key, gmt_offset
  
### get_drivers:
Retrieve driver information. Can get all current drivers or filter by session_key to get drivers who participated in a specific session. Returns driver details including name, number, team, country, and headshot URL.

    Parameter	    	Description
    session_key	    	Optional. Filter drivers by session_key to get participants from a specific session.
    driver_number	   	Optional. Filter by driver number (e.g., 1, 44, 16).
    team_name        	Optional. Filter by team name (e.g., 'Red Bull Racing', 'Ferrari').
  
### get_laps:
Retrieve pit stop data for specific sessions. Returns detailed pit stop information including duration, lap number, and timing.

    Parameter	    	Description
    session_key	        Required for meaningful results. Filter by the unique session key.
    driver_number		Optional. Filter by driver number (e.g., 1, 44, 16).
    pit_duration		Optional. Upper bound for pit duration in seconds (e.g., 30.0 for stops under 30 seconds).

### overtakes:
Retrieve overtake data showing position changes between drivers. An overtake refers to one driver (the overtaking driver) exchanging positions with another driver (the overtaken driver). Returns detailed information including the drivers involved, the lap number, and the timing of the event.

    Parameter	                Description
    session_key	    	        Required for meaningful results. Filter by the unique session key.
    overtaking_driver_number    Optional. Filter by the driver number of the driver who performed the overtake (e.g., 1, 44).
    overtaken_driver_number		Optional. Filter by the driver number of the driver who was overtaken (e.g., 16, 63).

<br>

# Installation instructions:

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

- ### Overtakes related usage examples
    - "Show me all overtakes from the Monaco 2024 race"
      
    - "How many times did driver 1 overtake someone in session 9158?"
    
    - "Who overtook driver 44 in the last race?"
    
    - "Show me all overtakes involving driver 16"
    
    - "Which lap had the most overtakes in session 9158?"
    
    - "Show me all battles between drivers 1 and 16" (can use both parameters)

<br>

The server handles the API calls to OpenF1 and returns formatted data that Claude can interpret and present to you

<br>



  
