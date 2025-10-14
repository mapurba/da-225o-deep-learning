import json
import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from remote_mcp_agent.prompt import NOTION_PROMPT

# ---- MCP Library ----
# https://github.com/modelcontextprotocol/servers
# https://smithery.ai/

# ---- Notion -----
# https://developers.notion.com/docs/mcp
# https://github.com/makenotion/notion-mcp-server
# https://github.com/makenotion/notion-mcp-server/blob/main/scripts/notion-openapi.json

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if NOTION_API_KEY is None:
    raise ValueError("NOTION_API_KEY is not set")

NOTION_MCP_HEADERS = json.dumps(
    {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}
)

# --- Agent Definition ---

# Initialize the main agent instance.
root_agent = Agent(
    # Specify the Large Language Model (LLM) for reasoning.
    model="gemini-2.5-flash",

    # Assign a descriptive name to the agent.
    name="Notion_MCP_Agent",

    # Provide the agent with its core instructions and purpose.
    instruction=NOTION_PROMPT,

    # Define the list of tools available to the agent.
    tools=[
        # Equip the agent with a set of tools provided via the Model Context Protocol (MCP).
        MCPToolset(
            # Define the parameters for connecting to the MCP server.
            connection_params=StdioServerParameters(
                # The command to run to start the server (a Node.js package runner).
                command="npx",

                # The arguments for the command: run the official Notion MCP server package.
                args=["-y", "@notionhq/notion-mcp-server"],

                # Pass environment variables to the server process, including authentication headers.
                env={"OPENAPI_MCP_HEADERS": NOTION_MCP_HEADERS},
            )
        ),
    ],
    
)
