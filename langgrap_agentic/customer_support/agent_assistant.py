from dotenv import load_dotenv
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

# .env load
load_dotenv()

#import state
from  agent_state import State

#import tools
from flight_tool import(fetch_user_flight_information,search_flights,update_ticket_to_new_flight,cancel_ticket)
from car_rental_tool import(search_car_rentals,update_car_rental,book_car_rental,cancel_car_rental)
from lookup_policy_tool import (lookup_policy)
from hotel_tool import (search_hotels,update_hotel,book_hotel,cancel_hotel)
from excursions_tool import ( search_trip_recommendations,book_excursion,update_excursion,cancel_excursion)

# create assistant agent
class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:

            # part 1 -code start----------------------------
            # configuration = config.get("configurable", {})
            # passenger_id = configuration.get("passenger_id", None)
            # state = {**state, "user_info": passenger_id}
            # result = self.runnable.invoke(state)
            # part 1 -code end-----------------------------
            
            result = self.runnable.invoke(state)

            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
    

llm = ChatOpenAI(model="gpt-4-turbo", temperature=1)


primay_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful customer support assistant for Swiss Airlines. "
            " Use the provided tools to search for flights, company policies, and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

tools = [
    TavilySearchResults(max_results=1),
    fetch_user_flight_information,
    search_flights,
    lookup_policy,
    update_ticket_to_new_flight,
    cancel_ticket,
    search_car_rentals,
    book_car_rental,
    update_car_rental,
    cancel_car_rental,
    search_hotels,
    book_hotel,
    update_hotel,
    cancel_hotel,
    search_trip_recommendations,
    book_excursion,
    update_excursion,
    cancel_excursion
]

assistant_runnable = primay_assistant_prompt | llm.bind_tools(tools)
