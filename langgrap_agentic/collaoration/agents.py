import functools
from typing import Literal

from langgraph.prebuilt import ToolNode

from llm_model import llm
from agent_tools import (travily_tool as search_tool,python_repl)
from utilities import (agent_node,create_agent)


# Research agent and node
research_agent = create_agent(
    llm,
    [search_tool],
    system_message="""
                        You are an AI chat assistant specializing in research.
                        Your task is to gather and provide accurate and relevant data for the chart_generator to use. 
                        Ensure the data is up-to-date, applicable to real-world scenarios, and answer any research-related queries.
                    """,
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# chart_generator
chart_agent = create_agent(
    llm,
    [python_repl],
    system_message="Your primary purpose is to generate charts and graphs based on user data, ensuring they are applicable to real-world scenarios.",
)
chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")


# defind tools node
tools= [search_tool,python_repl]
tool_node = ToolNode(tools=tools)


# define edge logic
def router(state) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "__end__"
    return "continue"