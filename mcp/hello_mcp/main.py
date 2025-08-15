from mcp.server.fastmcp import FastMCP #type:ignore

mcp = FastMCP(name="hello mcp", stateless_http=True)

mcp_app =mcp.streamable_http_app()


@mcp.tool()
def sreach_online(query: str)-> str:
    return f"Result for {query}"

@mcp.tool()
async def get_weather(city: str)-> str:
    return f"Weather in {city} is sunny"