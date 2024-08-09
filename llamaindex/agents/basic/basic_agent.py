from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings , set_global_handler
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse

import os
# load .env
load_dotenv()


# os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "api_key=a8bd662d3c82b0f3391:827b9b0"
# os.environ["PHOENIX_CLIENT_HEADERS"] = "api_key=a8bd662d3c82b0f3391:827b9b0"
# os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
  

# Phoenix can display in real time the traces automatically
# collected from your LlamaIndex application.
# Run all of your LlamaIndex applications as usual and traces
# will be collected and displayed in Phoenix.

# setup Arize Phoenix for logging/observability
import llama_index.core
import os


PHOENIX_API_KEY = "a8bd662d3c82b0f3391:827b9b0"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
llama_index.core.set_global_handler(
    "arize_phoenix", endpoint="https://llamatrace.com/v1/traces"
)

...

# Defind LLM Models
# llm = OpenAI(model="gpt-4-turbo", temperature=0)
# llm = Ollama(model="llama3.1", request_timeout=120.0)
Settings.llm =   OpenAI(model="gpt-4-turbo", temperature=0)


# create funcitons
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b


def sub(a: float, b: float) -> float:
    """Subtract two numbers and return the difference."""
    return a - b


# funcitons as tools
multiply_tool = FunctionTool.from_defaults(fn=multiply)
subtract_tool = FunctionTool.from_defaults(fn=sub)
add_tool = FunctionTool.from_defaults(fn=add)

# # documents loader
# documents = SimpleDirectoryReader("./data").load_data()
# index = VectorStoreIndex.from_documents(documents)
# query_engine = index.as_query_engine()

# response = query_engine.query(
#     "How much exactly was allocated to a tax credit to promote investment in green technologies in the 2023 Canadian federal budget?"
# )
# print(response)

documents = LlamaParse(result_type="markdown").load_data(
    "./data/2023_canadian_budget.pdf"
)
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# query engin as tool
budget_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="canadian_budget_2023",
    description="A RAG engine with some basic facts about the 2023 Canadian federal budget.",
)

# create agent
agent = ReActAgent.from_tools(
    [multiply_tool, add_tool, subtract_tool, budget_tool], verbose=True
)

response = agent.chat(
    "What is the total amount of the 2023 Canadian federal budget multiplied by 3?"
    "Go step by step, using a tool to do any math."
    "Subtract by 1M."
)

print(response)
