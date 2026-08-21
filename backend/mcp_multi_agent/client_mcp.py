from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:

    def __init__(self):

        self.server_params = StdioServerParameters(
            command="python",
            args=["backend/mcp_single_client/server.py"],
        )

    async def execute(self, tool_name: str, state: dict):

        async with stdio_client(self.server_params) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments={
                        "state": state
                    },
                )

                return result


mcp_client = MCPClient()
