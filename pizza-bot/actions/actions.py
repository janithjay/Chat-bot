from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient


class ActionRecommendProfessionalHelp(Action):
    def name(self) -> Text:
        return "action_recommend_professional_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the entity from the user's message
        professional_type = next(tracker.get_latest_entity_values("professional_type"), None)

        # Define recommendations for different professionals
        recommendations = {
            "therapist": "You can find licensed therapists through platforms like BetterHelp or Talkspace.",
            "counselor": "Consider reaching out to local counseling centers or community mental health services.",
            "psychiatrist": "Psychiatrists can be found through referrals from your primary doctor or mental health clinics.",
            "psychologist": "Check out the American Psychological Association's website for a list of certified psychologists.",
            "life coach": "Explore platforms like LifeCoach.com or local directories for life coaching services."
        }

        # Prepare a response based on the professional type
        if professional_type in recommendations:
            response = recommendations[professional_type]
        else:
            response = (
                "I'm here to help, but I couldn't identify the professional you are looking for. "
                "Could you specify whether you need a therapist, counselor, psychiatrist, psychologist, or life coach?"
            )

        # Send the response
        dispatcher.utter_message(text=response)
        return []
    
class ActionGiveOutletDetails(Action):
    def name(self) -> Text:
        return "action_location_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the location entity from the user's message
        location = next(tracker.get_latest_entity_values("location"), None)

        # Check if the location entity is present
        if not location:
            dispatcher.utter_message(text="I couldn't understand the location. Could you specify it again?")
            return []

        # Connect to MongoDB
        try:
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")  # Update with your MongoDB URI
            db = client["pizza-bot"]  # Replace with your database name
            collection = db["contact_details"]  # Replace with your collection name

            # Query the database for the location
            result = collection.find_one({"Location": {"$regex": f"^{location}$", "$options": "i"}})

            if result:
                # Format the response using data from the database
                response = (
                    f"Here are the details for {location}:\n"
                    f"- Address: {result.get('Address', 'Not available')}\n"
                    f"- Telephone: {result.get('Telephone', 'Not available')}"
                )
            else:
                response = f"Sorry, I couldn't find any details for the location '{location}'."

        except Exception as e:
            response = "I'm having trouble connecting to the database. Please try again later."
            print(f"Database connection error: {e}")

        # Send the response
        dispatcher.utter_message(text=response)
        return []
    
class ActionProvideMenu(Action):
    def name(self) -> Text:
        return "action_provide_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Connect to MongoDB
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["pizza_menu"]

            # Fetch all pizzas
            pizzas = collection.find()
            
            if pizzas:
                response = "Here is our menu:\n"
                for pizza in pizzas:
                    response += f"- {pizza['Pizza']}:\n"
                    for size in ["Large", "Medium", "Personal", "Regular"]:
                        if pizza.get(size) != "Not Available":
                            response += f"  * \t{size}: {pizza[size]}\n"
            else:
                response = "Sorry, the menu is currently unavailable."

        except Exception as e:
            response = "I'm having trouble connecting to the database. Please try again later."
            print(f"Database connection error: {e}")

        # Send the response
        dispatcher.utter_message(text=response)
        return []

class ActionProvidePizzaDetails(Action):
    def name(self) -> Text:
        return "action_provide_pizza_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract the pizza entity from the user's message
        pizza_name = next(tracker.get_latest_entity_values("pizza"), None)

        if not pizza_name:
            dispatcher.utter_message(text="I couldn't understand the pizza name. Could you specify it again?")
            return []

        try:
            # Connect to MongoDB
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["pizza_menu"]

            # Query the database for the pizza
            pizza = collection.find_one({"Pizza": {"$regex": f"^{pizza_name}$", "$options": "i"}})

            if pizza:
                response = (
                    f"Here are the details for {pizza['Pizza']}:\n"
                    f"- Description: {pizza.get('Description', 'Not available')}\n"
                    f"- Prices:\n"
                )
                for size in ["Large", "Medium", "Personal", "Regular"]:
                    if pizza.get(size) != "Not Available":
                        response += f"  * \t{size}: {pizza[size]}\n"
            else:
                response = f"Sorry, I couldn't find any details for the pizza '{pizza_name}'."

        except Exception as e:
            response = "I'm having trouble connecting to the database. Please try again later."
            print(f"Database connection error: {e}")

        # Send the response
        dispatcher.utter_message(text=response)
        return []