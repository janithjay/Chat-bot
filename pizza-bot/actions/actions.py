from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient

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
                    f"Here are the details for {location} outlet:\n"
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
                response = "Here is our menu: (All price are in Rs.)\n"
                for pizza in pizzas:
                    response += f"- {pizza['Pizza']}:\n"
                    for size in ["Large", "Medium", "Personal", "Regular"]:
                        if pizza.get(size) != "Not Available":
                            response += f"  * \t{size:<8}: {pizza[size]:>6}\n"
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
                    f"- {pizza.get('Description', 'Not available')}\n"
                    f"- Prices (Rs.):\n"
                )
                for size in ["Large", "Medium", "Personal", "Regular"]:
                    if pizza.get(size) != "Not Available":
                        response += f"  * \t{size:<8}: {pizza[size]:>6}\n"
            else:
                response = f"Sorry, I couldn't find any details for the pizza '{pizza_name}'."

        except Exception as e:
            response = "I'm having trouble connecting to the database. Please try again later."
            print(f"Database connection error: {e}")

        # Send the response
        dispatcher.utter_message(text=response)
        return []
    
class ActionProvideDrinksMenu(Action):
    def name(self) -> Text:
        return "action_provide_drinks_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Connect to MongoDB
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["drinks_menu"]

            # Fetch all drinks
            drinks = collection.find()
            
            if drinks:
                response = "Here is our drinks menu: (All price are in Rs.)\n"
                for drink in drinks:
                    # Drink name and price formatting to make sure they are aligned
                    response += f"- {drink['Drink']:<30}: {drink['Price']:>6} LKR\n"
            else:
                response = "Sorry, the drinks menu is currently unavailable."

        except Exception as e:
            response = "I'm having trouble connecting to the database. Please try again later."
            print(f"Database connection error: {e}")

        # Send the response
        dispatcher.utter_message(text=response)
        return []