from agent_graph import super_graph

from langchain_core.messages import HumanMessage

for s in super_graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Write a brief research report in Myanmar economy. Include a chart."
            )
        ],
    },
    {"recursion_limit": 150},
):
    if "__end__" not in s:
            print(s)