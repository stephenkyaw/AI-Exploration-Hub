from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()

class EmployeeInfo(TypedDict):
    name: str
    position: str
    document: str

@tool
def get_employee_info(name: str, position: str, document: str) -> EmployeeInfo:
    """
    Create an employee information object.

    Args:
        name (str): The employee's name.
        position (str): The employee's position.
        document (str): A document related to the employee (e.g., ID, certificate).

    Returns:
        EmployeeInfo: A dictionary containing the employee's name, position, and document.
    """
    
    # Validate inputs
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Invalid name: must be a non-empty string.")
    if not isinstance(position, str) or not position.strip():
        raise ValueError("Invalid position: must be a non-empty string.")
    if not isinstance(document, str) or not document.strip():
        raise ValueError("Invalid document: must be a non-empty string.")
    
    employee_info = EmployeeInfo(name=name, position=position, document=document)
    return employee_info

tools = [get_employee_info]
tool_node = ToolNode(tools)


llm = ChatOpenAI(model="gpt-4-turbo").bind_tools(tools)


response = llm.invoke("My name is Kyaw Myo Aung and I am software developer.Please create employee object.")

print(response)

