from fastmcp import FastMCP
import sqlite3
import sys
import os
import requests
import json
""" supports multiple APIs"""
mcp = FastMCP("multitool_server")  

@mcp.tool()
def query(query: str) -> str:
    """Queries a Sqlite3 restaurant database. Returns the result of the query."""
    """Sample query: show restaurants in Portland from table restaurants"""
    database = "db_data/entries.db"
    con = sqlite3.connect(database)
    cur = con.cursor()
    results = cur.execute(query)
    con.commit()
    output_string = '\n'.join([', '.join(map(str, row)) for row in results])
    return output_string

@mcp.tool()
def geocode(query: str) -> str:
    """Use Google Maps Geocoding API to find information about an address.
       Example: Find the address of Portland State University in Portland
    """

    API_KEY = os.environ.get("API_KEY")
    if not API_KEY:
        return "Error: Missing Google Maps API key"

    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": query, "key": API_KEY}
        )
        data = resp.json()
        return json.dumps(data, indent=2)

    except Exception as e:
        return f"Geocode API error: {e}"

"""Use Yelp Api to lookup areas of interest based on terms and locations
    Example: Use the Yelp tool to find businesses matching coffee in Portland, OR""" 
@mcp.tool()
def yelp_search(term: str, location: str) -> str:
    """ this is the API key variable set in Cloud Run-- not actually stored in this source file """
    api_key = os.environ.get("YELP_API_KEY")
    """ URL is built using Business search endpoint """
    url = f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}&limit=3"
    headers = {"Authorization": f"Bearer {api_key}"}
    """ response contains the JSON response from Yelp's validation""" 
    response = requests.get(url, headers=headers)
    businesses = response.json().get("businesses", [])
    return "\n".join([f"{b['name']} - {b.get('rating','N/A')} stars" for b in businesses])
""" sets up HTTP MCP Server """
if __name__ == "__main__":
    """ cloud run listens on port 8080"""
    port = int(os.environ.get("PORT", "8080"))
    print(f"Starting MCP server on 0.0.0.0:{port}...")

    try:
        mcp.run(
            transport="http",
            host="0.0.0.0",
            port=port
        )
    except Exception as e:
        print(f"Server failed to start: {e}")


