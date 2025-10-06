"""
F1 Historical Data MCP Server

This MCP server provides access to historical Formula 1 race session and driver data
from the OpenF1 API (https://openf1.org/).

Tools:
- get_sessions: Retrieve F1 race sessions with optional filtering
- get_drivers: Retrieve driver information for all drivers or a specific session
- get_laps: Retrieve lap data for specific session/driver/lap combinations
- get_pit_stops: Retrieve pit stop data for specific sessions with optional duration filtering
- get_overtakes: Retrieve overtake data showing position changes between drivers
"""

import asyncio
import httpx
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


# API Base URL
BASE_URL = "https://api.openf1.org/v1"

# Initialize MCP server
app = Server("f1-historical-data")


async def fetch_data(endpoint: str, params: Optional[dict] = None) -> Any:
    """
    Fetch data from the OpenF1 API.
    
    Args:
        endpoint: API endpoint path
        params: Optional query parameters
        
    Returns:
        JSON response data
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{BASE_URL}/{endpoint}"
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the F1 data server."""
    return [
        Tool(
            name="get_sessions",
            description=(
                "Retrieve F1 race sessions. Can filter by year, country, circuit, session type, etc. "
                "Returns session details including session_key, date, location, and type. "
                "Available filters: year, country_name, circuit_short_name, session_name, session_type, "
                "session_key, date_start (>=, <=), location, country_code, meeting_key, gmt_offset."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Filter by year (e.g., 2023, 2024)"
                    },
                    "country_name": {
                        "type": "string",
                        "description": "Filter by country name (e.g., 'Monaco', 'Italy')"
                    },
                    "circuit_short_name": {
                        "type": "string",
                        "description": "Filter by circuit short name (e.g., 'Monza', 'Monaco')"
                    },
                    "session_name": {
                        "type": "string",
                        "description": "Filter by session name (e.g., 'Race', 'Qualifying', 'Sprint')"
                    },
                    "session_key": {
                        "type": "integer",
                        "description": "Get specific session by session_key"
                    },
                    "date_start": {
                        "type": "string",
                        "description": "Filter by start date (ISO format: YYYY-MM-DD)"
                    }
                }
            }
        ),
        Tool(
            name="get_drivers",
            description=(
                "Retrieve driver information. Can get all drivers or filter by session_key. "
                "Returns driver details including name, number, team, country, and headshot URL. "
                "If session_key is provided, returns drivers who participated in that specific session."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_key": {
                        "type": "integer",
                        "description": "Optional: Filter drivers by session_key to get drivers from a specific session"
                    },
                    "driver_number": {
                        "type": "integer",
                        "description": "Optional: Filter by driver number (e.g., 1, 44, 16)"
                    },
                    "team_name": {
                        "type": "string",
                        "description": "Optional: Filter by team name (e.g., 'Red Bull Racing', 'Ferrari')"
                    }
                }
            }
        ),
        Tool(
            name="get_laps",
            description=(
                "Retrieve lap data for specific sessions, drivers, and laps. "
                "Returns detailed lap information including lap time, sector times, duration, and position. "
                "Can filter by session_key, driver_number, lap_number, and other parameters."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_key": {
                        "type": "integer",
                        "description": "Filter by session_key (required for meaningful results)"
                    },
                    "driver_number": {
                        "type": "integer",
                        "description": "Filter by driver number (e.g., 1, 44, 16)"
                    },
                    "lap_number": {
                        "type": "integer",
                        "description": "Filter by specific lap number"
                    }
                }
            }
        ),
        Tool(
            name="get_pit_stops",
            description=(
                "Retrieve pit stop data for specific sessions. "
                "Returns detailed pit stop information including duration, lap number, and timing. "
                "Can filter by session_key, driver_number, and set upper bound on pit duration."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_key": {
                        "type": "integer",
                        "description": "Filter by session_key (required for meaningful results)"
                    },
                    "driver_number": {
                        "type": "integer",
                        "description": "Optional: Filter by driver number (e.g., 1, 44, 16)"
                    },
                    "pit_duration": {
                        "type": "number",
                        "description": "Optional: Upper bound for pit duration in seconds (e.g., 30.0 for stops under 30 seconds)"
                    }
                }
            }
        ),
        Tool(
            name="get_overtakes",
            description=(
                "Retrieve overtake data showing position changes between drivers. "
                "An overtake refers to one driver (overtaking driver) exchanging positions with another driver (overtaken driver). "
                "Returns detailed overtake information including drivers involved, lap number, and timing. "
                "Can filter by session_key, overtaking driver, and overtaken driver."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_key": {
                        "type": "integer",
                        "description": "Filter by session_key (required for meaningful results)"
                    },
                    "overtaking_driver_number": {
                        "type": "integer",
                        "description": "Optional: Filter by the driver number of the overtaking driver"
                    },
                    "overtaken_driver_number": {
                        "type": "integer",
                        "description": "Optional: Filter by the driver number of the overtaken driver"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for F1 data retrieval."""
    
    if name == "get_sessions":
        # Build query parameters from arguments
        params = {}
        
        if "year" in arguments:
            params["year"] = arguments["year"]
        if "country_name" in arguments:
            params["country_name"] = arguments["country_name"]
        if "circuit_short_name" in arguments:
            params["circuit_short_name"] = arguments["circuit_short_name"]
        if "session_name" in arguments:
            params["session_name"] = arguments["session_name"]
        if "session_key" in arguments:
            params["session_key"] = arguments["session_key"]
        if "date_start" in arguments:
            params["date_start"] = arguments["date_start"]
        
        try:
            sessions = await fetch_data("sessions", params)
            
            if not sessions:
                return [TextContent(
                    type="text",
                    text="No sessions found matching the criteria."
                )]
            
            # Format the response
            result = f"Found {len(sessions)} session(s):\n\n"
            for session in sessions:
                result += f"Session Key: {session.get('session_key')}\n"
                result += f"Name: {session.get('session_name')}\n"
                result += f"Type: {session.get('session_type')}\n"
                result += f"Date: {session.get('date_start')}\n"
                result += f"Location: {session.get('location')}\n"
                result += f"Country: {session.get('country_name')}\n"
                result += f"Circuit: {session.get('circuit_short_name')}\n"
                result += f"Year: {session.get('year')}\n"
                result += f"Meeting Key: {session.get('meeting_key')}\n"
                result += "-" * 50 + "\n\n"
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error fetching sessions: {str(e)}"
            )]
    
    elif name == "get_drivers":
        # Build query parameters from arguments
        params = {}
        
        if "session_key" in arguments:
            params["session_key"] = arguments["session_key"]
        if "driver_number" in arguments:
            params["driver_number"] = arguments["driver_number"]
        if "team_name" in arguments:
            params["team_name"] = arguments["team_name"]
        
        try:
            drivers = await fetch_data("drivers", params)
            
            if not drivers:
                return [TextContent(
                    type="text",
                    text="No drivers found matching the criteria."
                )]
            
            # Format the response
            session_info = f" for session {arguments['session_key']}" if "session_key" in arguments else ""
            result = f"Found {len(drivers)} driver(s){session_info}:\n\n"
            
            for driver in drivers:
                result += f"Driver Number: {driver.get('driver_number')}\n"
                result += f"Name: {driver.get('full_name')}\n"
                result += f"Abbreviation: {driver.get('name_acronym')}\n"
                result += f"Team: {driver.get('team_name')}\n"
                result += f"Country: {driver.get('country_code')}\n"
                result += f"Headshot: {driver.get('headshot_url')}\n"
                if "session_key" in driver:
                    result += f"Session Key: {driver.get('session_key')}\n"
                result += "-" * 50 + "\n\n"
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error fetching drivers: {str(e)}"
            )]
    
    elif name == "get_laps":
        # Build query parameters from arguments
        params = {}
        
        if "session_key" in arguments:
            params["session_key"] = arguments["session_key"]
        if "driver_number" in arguments:
            params["driver_number"] = arguments["driver_number"]
        if "lap_number" in arguments:
            params["lap_number"] = arguments["lap_number"]
        
        try:
            laps = await fetch_data("laps", params)
            
            if not laps:
                return [TextContent(
                    type="text",
                    text="No lap data found matching the criteria."
                )]
            
            # Format the response
            filters = []
            if "session_key" in arguments:
                filters.append(f"session {arguments['session_key']}")
            if "driver_number" in arguments:
                filters.append(f"driver #{arguments['driver_number']}")
            if "lap_number" in arguments:
                filters.append(f"lap {arguments['lap_number']}")
            
            filter_str = " for " + ", ".join(filters) if filters else ""
            result = f"Found {len(laps)} lap(s){filter_str}:\n\n"
            
            for lap in laps:
                result += f"Lap Number: {lap.get('lap_number')}\n"
                result += f"Driver Number: {lap.get('driver_number')}\n"
                result += f"Session Key: {lap.get('session_key')}\n"
                
                if lap.get('lap_duration'):
                    result += f"Lap Duration: {lap.get('lap_duration')} seconds\n"
                if lap.get('duration_sector_1'):
                    result += f"Sector 1: {lap.get('duration_sector_1')} seconds\n"
                if lap.get('duration_sector_2'):
                    result += f"Sector 2: {lap.get('duration_sector_2')} seconds\n"
                if lap.get('duration_sector_3'):
                    result += f"Sector 3: {lap.get('duration_sector_3')} seconds\n"
                
                if lap.get('segments_sector_1'):
                    result += f"Sector 1 Segments: {lap.get('segments_sector_1')}\n"
                if lap.get('segments_sector_2'):
                    result += f"Sector 2 Segments: {lap.get('segments_sector_2')}\n"
                if lap.get('segments_sector_3'):
                    result += f"Sector 3 Segments: {lap.get('segments_sector_3')}\n"
                
                if lap.get('i1_speed') is not None:
                    result += f"Speed Trap 1 (I1): {lap.get('i1_speed')} km/h\n"
                if lap.get('i2_speed') is not None:
                    result += f"Speed Trap 2 (I2): {lap.get('i2_speed')} km/h\n"
                if lap.get('st_speed') is not None:
                    result += f"Speed Trap (ST): {lap.get('st_speed')} km/h\n"
                
                if lap.get('is_pit_out_lap') is not None:
                    result += f"Pit Out Lap: {lap.get('is_pit_out_lap')}\n"
                
                if lap.get('date_start'):
                    result += f"Start Time: {lap.get('date_start')}\n"
                
                result += "-" * 50 + "\n\n"
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error fetching lap data: {str(e)}"
            )]
    
    elif name == "get_pit_stops":
        # Build query parameters from arguments
        params = {}
        
        if "session_key" in arguments:
            params["session_key"] = arguments["session_key"]
        if "driver_number" in arguments:
            params["driver_number"] = arguments["driver_number"]
        if "pit_duration" in arguments:
            # Use <= operator for upper bound
            params["pit_duration"] = f"<={arguments['pit_duration']}"
        
        try:
            pit_stops = await fetch_data("pit", params)
            
            if not pit_stops:
                return [TextContent(
                    type="text",
                    text="No pit stop data found matching the criteria."
                )]
            
            # Format the response
            filters = []
            if "session_key" in arguments:
                filters.append(f"session {arguments['session_key']}")
            if "driver_number" in arguments:
                filters.append(f"driver #{arguments['driver_number']}")
            if "pit_duration" in arguments:
                filters.append(f"duration ≤ {arguments['pit_duration']}s")
            
            filter_str = " for " + ", ".join(filters) if filters else ""
            result = f"Found {len(pit_stops)} pit stop(s){filter_str}:\n\n"
            
            for pit in pit_stops:
                result += f"Driver Number: {pit.get('driver_number')}\n"
                result += f"Session Key: {pit.get('session_key')}\n"
                result += f"Lap Number: {pit.get('lap_number')}\n"
                
                if pit.get('pit_duration') is not None:
                    result += f"Pit Duration: {pit.get('pit_duration')} seconds\n"
                
                if pit.get('date'):
                    result += f"Time: {pit.get('date')}\n"
                
                if pit.get('meeting_key') is not None:
                    result += f"Meeting Key: {pit.get('meeting_key')}\n"
                
                result += "-" * 50 + "\n\n"
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error fetching pit stop data: {str(e)}"
            )]
    
    elif name == "get_overtakes":
        # Build query parameters from arguments
        params = {}
        
        if "session_key" in arguments:
            params["session_key"] = arguments["session_key"]
        if "overtaking_driver_number" in arguments:
            params["overtaking_driver_number"] = arguments["overtaking_driver_number"]
        if "overtaken_driver_number" in arguments:
            params["overtaken_driver_number"] = arguments["overtaken_driver_number"]
        
        try:
            overtakes = await fetch_data("overtakes", params)
            
            if not overtakes:
                return [TextContent(
                    type="text",
                    text="No overtake data found matching the criteria."
                )]
            
            # Format the response
            filters = []
            if "session_key" in arguments:
                filters.append(f"session {arguments['session_key']}")
            if "overtaking_driver_number" in arguments:
                filters.append(f"overtaking driver #{arguments['overtaking_driver_number']}")
            if "overtaken_driver_number" in arguments:
                filters.append(f"overtaken driver #{arguments['overtaken_driver_number']}")
            
            filter_str = " for " + ", ".join(filters) if filters else ""
            result = f"Found {len(overtakes)} overtake(s){filter_str}:\n\n"
            
            for overtake in overtakes:
                result += f"Overtaking Driver: #{overtake.get('overtaking_driver_number')}\n"
                result += f"Overtaken Driver: #{overtake.get('overtaken_driver_number')}\n"
                result += f"Session Key: {overtake.get('session_key')}\n"
                
                if overtake.get('lap_number') is not None:
                    result += f"Lap Number: {overtake.get('lap_number')}\n"
                
                if overtake.get('date'):
                    result += f"Time: {overtake.get('date')}\n"
                
                if overtake.get('meeting_key') is not None:
                    result += f"Meeting Key: {overtake.get('meeting_key')}\n"
                
                result += "-" * 50 + "\n\n"
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error fetching overtake data: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
