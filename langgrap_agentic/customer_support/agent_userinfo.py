from agent_state import State
from flight_tool import fetch_user_flight_information



def user_info(state: State):
    return {"user_info":fetch_user_flight_information.invoke({})}


