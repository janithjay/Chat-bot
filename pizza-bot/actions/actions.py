from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop
from rasa_sdk.types import DomainDict
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

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
        extra_toppings = tracker.get_slot("extra_toppings")
        
        if pizza_type and pizza_size and pizza_crust:
            # Enhanced order confirmation with toppings
            order_details = (
                f"🍕 Order Confirmation:\n"
                f"• Pizza Type: {pizza_type.capitalize()}\n"
                f"• Size: {pizza_size.capitalize()}\n"
                f"• Crust: {pizza_crust.capitalize()}\n"
            )
            
            # Add toppings if specified
            if extra_toppings:
                order_details += f"• Extra Toppings: {extra_toppings.capitalize()}\n"
            
            order_details += "Estimated delivery time: 30-45 minutes"
            
            dispatcher.utter_message(text=order_details)
            dispatcher.utter_message(text="Your order has been sent to our kitchen. Thank you!")
            
            # Reset slots after successful order
            return [
                SlotSet("pizza_type", None),
                SlotSet("pizza_size", None),
                SlotSet("pizza_crust", None),
                SlotSet("extra_toppings", None),
                ActiveLoop(None)
            ]
        else:
            dispatcher.utter_message(text="Oops! Some details are missing. Let's start the order again.")
            return [ActiveLoop("pizza_order_form")]

class PriceAction(Action):
    def name(self) -> Text:
        return "action_ask_price"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        prices = (
            "🍕 Pizza Prices:\n"
            "• Small Pizza: $8.99\n"
            "• Medium Pizza: $11.99\n"
            "• Large Pizza: $14.99\n"
            "• Extra Toppings: $1.50 each"
        )
        dispatcher.utter_message(text=prices)
        return []

class HoursAction(Action):
    def name(self) -> Text:
        return "action_ask_hours"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        hours = (
            "🕰️ Business Hours:\n"
            "• Monday-Thursday: 11am - 10pm\n"
            "• Friday-Saturday: 11am - 12am\n"
            "• Sunday: 12pm - 9pm\n"
            "Delivery available during all hours!"
        )
        dispatcher.utter_message(text=hours)
        return []

class LocationAction(Action):
    def name(self) -> Text:
        return "action_ask_location"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = (
            "📍 Our Location:\n"
            "123 Pizza Street\n"
            "Delicious City, Pizza State 12345\n"
            "Phone: (555) PIZZA-YUM\n"
            "We offer both pickup and delivery!"
        )
        dispatcher.utter_message(text=location)
        return []

class MenuAction(Action):
    def name(self) -> Text:
        return "action_show_menu"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        menu = (
            "🍽️ Our Pizza Menu:\n"
            "Classic Pizzas:\n"
            "• Pepperoni: Loaded with pepperoni slices\n"
            "• Margherita: Fresh mozzarella, basil, tomato sauce\n"
            "• Vegetarian: Bell peppers, mushrooms, olives\n"
            "• Supreme: Pepperoni, sausage, peppers, onions\n"
            "• Hawaiian: Ham and pineapple\n\n"
            "Toppings:\n"
            "• Meats: Pepperoni, Sausage, Bacon, Ham\n"
            "• Veggies: Mushrooms, Olives, Onions, Peppers\n"
            "• Cheese: Extra Cheese, Feta, Parmesan"
        )
        dispatcher.utter_message(text=menu)
        return []

class AddToppingsAction(Action):
    def name(self) -> Text:
        return "action_add_toppings"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        extra_toppings = tracker.get_slot("extra_toppings")
        
        if extra_toppings:
            dispatcher.utter_message(
                text=f"Great! I'll add {extra_toppings} to your pizza. Each extra topping is $1.50."
            )
            return [SlotSet("extra_toppings", extra_toppings)]
        else:
            dispatcher.utter_message(
                text="You can add various toppings like mushrooms, extra cheese, olives, and more!"
            )
            return []

class PizzaOrderFormValidationAction(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_order_form"

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        valid_types = ["pepperoni", "margherita", "vegetarian", "supreme", "hawaiian"]
        pizza_type = slot_value.lower() if isinstance(slot_value, str) else None
        
        if pizza_type in valid_types:
            return {"pizza_type": pizza_type}
        
        dispatcher.utter_message(text=f"We have {', '.join(valid_types)} pizzas. Please choose one of these.")
        return {"pizza_type": None}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        valid_sizes = ["small", "medium", "large"]
        pizza_size = slot_value.lower() if isinstance(slot_value, str) else None
        
        if pizza_size in valid_sizes:
            return {"pizza_size": pizza_size}
        
        dispatcher.utter_message(text=f"Please choose a size: {', '.join(valid_sizes)}.")
        return {"pizza_size": None}

    def validate_pizza_crust(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        valid_crusts = ["thin", "thick", "regular", "stuffed", "hand-tossed"]
        pizza_crust = slot_value.lower() if isinstance(slot_value, str) else None
        
        if pizza_crust in valid_crusts:
            return {"pizza_crust": pizza_crust}
        
        dispatcher.utter_message(text=f"Crust options are: {', '.join(valid_crusts)}.")
        return {"pizza_crust": None}