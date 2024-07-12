from typing import Literal

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition

from agent_state import State
from agent_assistant import (Assistant,assistant_runnable)
from agent_userinfo import user_info
from utilities import (create_tool_node_with_fallback)

from agent_tools import (safe_tools,sensitive_tools,sensitive_tool_names)

builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("fetch_user_info",user_info)
builder.add_edge(START,"fetch_user_info")
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("safe_tools", create_tool_node_with_fallback(tools=safe_tools))
builder.add_node("sensitive_tools", create_tool_node_with_fallback(tools=sensitive_tools))


# Define logic
builder.add_edge("fetch_user_info","assistant")

def route_tools(state: State) -> Literal["safe_tools", "sensitive_tools", "__end__"]:
    next_node = tools_condition(state)
    # If no tools are invoked, return to the user
    if next_node == END:
        return END
    ai_message = state["messages"][-1]
    # This assumes single tool calls. To handle parallel tool calling, you'd want to
    # use an ANY condition
    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call["name"] in sensitive_tool_names:
        return "sensitive_tools"
    return "safe_tools"



# Define edges: these determine how the control flow moves
builder.add_conditional_edges(
    "assistant",
    route_tools,
)
builder.add_edge("safe_tools", "assistant")
builder.add_edge("sensitive_tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = SqliteSaver.from_conn_string(":memory:")
graph = builder.compile(checkpointer=memory, interrupt_before=["sensitive_tools"])
