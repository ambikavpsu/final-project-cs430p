"""
This is the MCP client that supports the usage of multiple APIs
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio
llm = ChatGoogleGenerativeAI(
             model=os.getenv("GOOGLE_MODEL"),
             safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )

"""
The given prompt is read by an LLM so it understands what should be done with a user query
"""
prompt = f"You are a multi-tool agent which relies on an MCP server. These are the available tools: SQlite database queries, Google Maps Geocoding address, Yelp search tool. Your role is to understand the user's query (natural language request), identify the tools needed based on the query, calling the tools with valid arguments, combining results of multiple tools if needed, and returning a clear answer to the user. Do NOT assume every request is SQL"
async def run_agent():
    """ opens an MCP HTTP connection to the server """ 
    async with streamablehttp_client(f"{os.getenv('MCP_URL')}/mcp") as (read, write, _):
        """creates the client session """
        async with ClientSession(read, write) as session:
            """asks the server what tools are from the API """
            await session.initialize()

            tools = await load_mcp_tools(session)
            """creates ReAct agent """

            agent = create_agent(model=llm, tools=tools, system_prompt=prompt, debug=True)

            print(f"Welcome to the multi-API agent (MCP). Ask me any question regarding 1. a restaurant database containing lists of restaurants 2. Finding a Google Maps location based on the description 3. Searching up areas of interest on Yelp based on location. It's possible to combine multiple APIs in one search") 
            """ REPL loop: sends user messages to the agent, agent calls tools when needed """
            while True:
                line = input("llm>> ")
                if line:
                    try:
                        """result includes messages and tool actions """
                        result = await agent.ainvoke({"messages": [("user", line)]})
                        # Extract the actual message content from the agent's response
                        if "messages" in result:
                            messages = result["messages"]
                            if messages:
                                last_message = messages[-1]
                                """ prints the final text """
                                if hasattr(last_message, 'content'):
                                    print(f"{last_message.content}")
                                else:
                                    print(f"{last_message}")
                            else:
                                print("No response from agent")
                        else:
                            print(f"Agent response: {result}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    break

"""entry point"""
if __name__ == "__main__":
    asyncio.run(run_agent())
