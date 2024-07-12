from langchain_community.tools.tavily_search import TavilySearchResults
#import tools
from flight_tool import(fetch_user_flight_information,search_flights,update_ticket_to_new_flight,cancel_ticket)
from car_rental_tool import(search_car_rentals,update_car_rental,book_car_rental,cancel_car_rental)
from lookup_policy_tool import (lookup_policy)
from hotel_tool import (search_hotels,update_hotel,book_hotel,cancel_hotel)
from excursions_tool import ( search_trip_recommendations,book_excursion,update_excursion,cancel_excursion)


 #"Read"-only tools (such as retrievers) don't need a user confirmation to use
safe_tools = [
    TavilySearchResults(max_results=1),
    fetch_user_flight_information,
    search_flights,
    lookup_policy,
    search_car_rentals,
    search_hotels,
    search_trip_recommendations,
]


# These tools all change the user's reservations.
# The user has the right to control what decisions are made
sensitive_tools = [
    update_ticket_to_new_flight,
    cancel_ticket,
    book_car_rental,
    update_car_rental,
    cancel_car_rental,
    book_hotel,
    update_hotel,
    cancel_hotel,
    book_excursion,
    update_excursion,
    cancel_excursion,
]

sensitive_tool_names = {t.name for t in sensitive_tools}
