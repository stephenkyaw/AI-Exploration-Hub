import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage

# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str