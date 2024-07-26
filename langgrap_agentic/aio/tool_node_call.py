import operator
from typing import Literal, TypedDict, List, Annotated
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import AnyMessage, SystemMessage
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import ToolNode, InjectedState
from langgraph.graph import StateGraph, MessagesState, add_messages, START,END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

#state: Annotated[dict, InjectedState]
@tool
def read_pdf(config: RunnableConfig, state: Annotated[dict, InjectedState]):
    """
    Reads a PDF file and returns the combined content of all pages.

    This function utilizes PyMuPDFLoader to load the PDF content and then extracts the text from each page.
    If the PDF cannot be read or the format is incorrect, an appropriate error message is returned.

    Parameters:
    - pdf_file_path (str): The file path to the PDF file to be read.

    Returns:
    - str: Combined text content of all pages of the PDF, or an error message if something goes wrong.

    Example:
    >>> content = read_pdf("path/to/resume.pdf")
    >>> print(content)
    """
    try:
        # Initialize the PDF loader
        loader = PyMuPDFLoader(state["resume_file_path"])
        # Load the PDF content
        data = loader.load()

        # Check if any pages were loaded
        if not data:
            return "No data found in the PDF file."

        # Ensure data is a list of Document objects with 'page_content' attributes
        if not isinstance(data, list) or not all(
            hasattr(page, "page_content") for page in data
        ):
            return "Invalid data format."

        # Combine content of all pages
        full_text = "\n\n".join(page.page_content for page in data)

        print("read_resume, read_pdf ============> ", state["read_resume"])

        return full_text

    except Exception as e:
        return f"An error occurred while reading the PDF: {e}"


tools = [read_pdf]
tool_node = ToolNode(tools)

llm = ChatOpenAI(model="gpt-4-turbo", temperature=1).bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    resume_file_path: str
    user_id : str
    read_resume : bool


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


def call_model(state: AgentState):
    """generated interview question from resume file."""

    messages = state["messages"]
    response = llm.invoke(messages)
    print("read_resume, call_model ============> ", state["read_resume"])
    return {"messages": [response]}


workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)
workflow.add_edge("action", "agent")

memory = MemorySaver()

app = workflow.compile(checkpointer=memory,interrupt_before=["action"])

input = {
    "messages": [
        {
            "role": "system",
            "content": """
                        You are an HR Interview Question Assistant agent. Your task is to generate specific and insightful interview questions for the interviewer based on the provided candidate's resume.

                        Guidelines for generating questions:
                        1. Focus on the key skills and experiences highlighted in the job description.
                        2. Emphasize the candidate's qualifications and relevant experiences as detailed in the resume.
                        3. Integrate any unique motivations or aspects mentioned in the cover letter.

                        Generate questions that:
                        - Assess technical skills and expertise relevant to the job.
                        - Explore past projects or experiences related to the role.
                        - Understand the candidate's motivation and fit for the company culture.

                        Tools provided: candidate's resume.
                    """,
        }
    ],
    "resume_file_path": "./data/resume.pdf",
    "read_resume" : False
}
configurable = {"configurable": {"user_id": "123", "thread_id": "1"}}

for chunk in app.stream(input, config=configurable, stream_mode="values"):
    chunk["messages"][-1].pretty_print()


app.update_state(configurable, {"read_resume": True})

for event in app.stream(None, configurable, stream_mode="values"):
    event["messages"][-1].pretty_print()