from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition

from agent_state import State
from agent_assistant import (Assistant,assistant_runnable,tools)
from agent_userinfo import user_info
from utilities import (create_tool_node_with_fallback)


builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("fetch_user_info",user_info)
builder.add_edge(START,"fetch_user_info")

builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools=tools))

builder.add_edge("fetch_user_info","assistant")

# Define edges: these determine how the control flow moves
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = SqliteSaver.from_conn_string(":memory:")
graph = builder.compile(checkpointer=memory, interrupt_before=["tools"])
