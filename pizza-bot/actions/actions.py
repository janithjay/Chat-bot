# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class PizzaOrderAction(Action):
    def name(self) -> Text:
        return "action_order_pizza"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        pizza_type = tracker.get_slot("pizza_type")
        pizza_size = tracker.get_slot("pizza_size")
        pizza_crust = tracker.get_slot("pizza_crust")
        
        if pizza_type and pizza_size and pizza_crust:
            order_details = (
                f"Order Details:\n"
                f"Pizza Type: {pizza_type}\n"
                f"Size: {pizza_size}\n"
                f"Crust: {pizza_crust}"
            )
            dispatcher.utter_message(text=order_details)
            dispatcher.utter_message(text="Your order is being processed!")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't complete your order. Please try again.")
        
        return []