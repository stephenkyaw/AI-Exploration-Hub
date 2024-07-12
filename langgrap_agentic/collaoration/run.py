from langchain_core.messages import HumanMessage
from agent_graph import graph

while True:
    print('User| type with quit or exit or q will closed :\n')
    user_input = input()
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    events = graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 150},
    )
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()