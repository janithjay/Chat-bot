from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop
from rasa_sdk.types import DomainDict

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
            # Enhanced order confirmation with more details
            order_details = (
                f"🍕 Order Confirmation:\n"
                f"• Pizza Type: {pizza_type.capitalize()}\n"
                f"• Size: {pizza_size.capitalize()}\n"
                f"• Crust: {pizza_crust.capitalize()}\n"
                f"Estimated delivery time: 30-45 minutes"
            )
            dispatcher.utter_message(text=order_details)
            dispatcher.utter_message(text="Your order has been sent to our kitchen. Thank you!")
            
            # Reset slots after successful order
            return [
                SlotSet("pizza_type", None),
                SlotSet("pizza_size", None),
                SlotSet("pizza_crust", None),
                ActiveLoop(None)
            ]
        else:
            dispatcher.utter_message(text="Oops! Some details are missing. Let's start the order again.")
            return [ActiveLoop("pizza_order_form")]

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
        valid_types = ["pepperoni", "margherita", "vegetarian"]
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
        valid_crusts = ["thin", "thick", "regular"]
        pizza_crust = slot_value.lower() if isinstance(slot_value, str) else None
        
        if pizza_crust in valid_crusts:
            return {"pizza_crust": pizza_crust}
        
        dispatcher.utter_message(text=f"Crust options are: {', '.join(valid_crusts)}.")
        return {"pizza_crust": None}

class AskQuestionAction(Action):
    def name(self) -> Text:
        return "action_gpt2_response"
    
    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_query = tracker.latest_message.get('text', '')
        
        # Simple predefined responses for different types of questions
        responses = {
            "ai": "AI is a technology that enables machines to learn and perform tasks that typically require human intelligence.",
            "machine learning": "Machine learning is a subset of AI where systems learn and improve from experience without being explicitly programmed.",
            "pizza": "We specialize in delicious pizzas with various types, sizes, and crusts. Would you like to order one?",
            "order": "To order a pizza, just say 'I want to order a pizza' and I'll guide you through the process.",
            "help": "I can help you order a pizza or answer questions about our service. Just ask!"
        }
        
        # Find the most relevant response
        response = next((resp for key, resp in responses.items() if key in user_query.lower()), 
                        "I'm not sure about that. Could you ask something related to pizza ordering?")
        
        dispatcher.utter_message(text=response)
        return []