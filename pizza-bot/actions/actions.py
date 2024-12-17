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
    
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')
        self.model.eval()  # Set the model to evaluation mode

    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_query = tracker.latest_message.get('text', '')
        
        # Generate a response using GPT-2
        input_ids = self.tokenizer.encode(user_query, return_tensors='pt')
        with torch.no_grad():
            output = self.model.generate(input_ids, max_length=50, num_return_sequences=1)
        
        # Decode the generated response
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Filter the response to ensure it's relevant to pizza ordering
        if "pizza" in response.lower() or "order" in response.lower():
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I'm not sure about that. Could you ask something related to pizza ordering?")
        
        return []