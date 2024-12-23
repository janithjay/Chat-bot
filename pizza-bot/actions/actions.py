from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from pymongo import MongoClient
from datetime import datetime
from rasa_sdk.types import DomainDict
import random
import string
from datetime import datetime

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
    
class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"

    def validate_contact(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value.isdigit() and len(slot_value) >= 10:
            dispatcher.utter_message(text="For which date would you like to make the reservation? (YYYY-MM-DD)")
            return {"contact": slot_value}
        dispatcher.utter_message(text="Please provide a valid contact number")
        return {"contact": None}

    def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        try:
            datetime.strptime(slot_value, '%Y-%m-%d')
            dispatcher.utter_message(text="Which city?")
            return {"date": slot_value}
        except ValueError:
            dispatcher.utter_message(text="Please provide date in YYYY-MM-DD format")
            return {"date": None}

class GenerateReservationID:
    @staticmethod
    def generate_id():
        # Generate random 4-digit number
        return ''.join(random.choices(string.digits, k=4))
    
    @staticmethod
    def check_unique(db, reservation_id):
        # Check if ID exists in database
        return db.reservations.find_one({"reservation_id": reservation_id}) is None

class SaveReservation(Action):
    def name(self) -> Text:
        return "action_save_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["reservations"]

            # Generate unique reservation ID
            while True:
                reservation_id = GenerateReservationID.generate_id()
                if GenerateReservationID.check_unique(db, reservation_id):
                    break

            reservation = {
                "reservation_id": reservation_id,
                "name": tracker.get_slot('name'),
                "contact": tracker.get_slot('contact'),
                "date": tracker.get_slot('date'),
                "city": tracker.get_slot('city'),
                "created_at": datetime.now()
            }

            collection.insert_one(reservation)

            response = (
                f"✅ Reservation Confirmed!\n"
                f"Your Reservation ID: {reservation_id}\n"
                f"Please keep this ID for future reference.\n\n"
                f"Reservation Details:\n"
                f"Name: {reservation['name']}\n"
                f"Contact: {reservation['contact']}\n"
                f"Date: {reservation['date']}\n"
                f"City: {reservation['city']}"
            )
            
            dispatcher.utter_message(text=response)
            return [
                    SlotSet("name", None),
                    SlotSet("contact", None),
                    SlotSet("date", None),
                    SlotSet("city", None),
                    SlotSet("reservation_id", None),
                ]
        
        except Exception as e:
            dispatcher.utter_message(text="Error saving reservation.")
            return []
        
class ReservationViewForm(FormValidationAction):
    def name(self) -> Text:
        return "action_reservation_view_form"

    def reservation_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value.isdigit() and len(slot_value) == 4:
            dispatcher.utter_message(text="Finding reservations for")
            return {"reservation_id": slot_value}
        dispatcher.utter_message(text="Please provide a valid reservation id")
        return {"reservation_id": None}

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        try:
            reservation_id = tracker.get_slot("reservation_id")
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["reservations"]
            
            reservation = collection.find_one({"reservation_id": reservation_id})
            
            if reservation:
                response = (
                    f"📋 Reservation Details:\n"
                    f"Reservation ID: {reservation['reservation_id']}\n"
                    f"Name: {reservation['name']}\n"
                    f"Contact: {reservation['contact']}\n"
                    f"Date: {reservation['date']}\n"
                    f"City: {reservation['city']}"
                )
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"❌ No reservation found with ID: {reservation_id}")
                
        except Exception as e:
            dispatcher.utter_message(text="Error retrieving reservation details.")
            
        return []
    
class ActionGetUpdatedDetails(Action):
    def name(self) -> Text:
        return "action_get_updated_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["reservations"]
            
            reservation_id = tracker.get_slot("reservation_id")
            reservation = collection.find_one({"reservation_id": reservation_id})
            
            if reservation:
                dispatcher.utter_message(text=f"Current reservation details:\n"
                                           f"Name: {reservation['name']}\n"
                                           f"Contact: {reservation['contact']}\n"
                                           f"Date: {reservation['date']}\n"
                                           f"City: {reservation['city']}\n"
                                           f"Please provide new details to update.")
                return [
                    SlotSet("name", None),
                    SlotSet("contact", None),
                    SlotSet("date", None),
                    SlotSet("city", None),
                ]
            else:
                dispatcher.utter_message(text=f"❌ No reservation found with ID: {reservation_id}")
                return []
                
        except Exception as e:
            dispatcher.utter_message(text="Error fetching reservation details.")
            return []

class ActionUpdateReservation(Action):
    def name(self) -> Text:
        return "action_update_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
            db = client["pizza-bot"]
            collection = db["reservations"]
            
            reservation_id = tracker.get_slot("reservation_id")
            name = tracker.get_slot("name")
            contact = tracker.get_slot("contact")
            date = tracker.get_slot("date")
            city = tracker.get_slot("city")
            
            if not all([reservation_id, name, contact, date, city]):
                dispatcher.utter_message(text="Missing required details for update.")
                return []
            
            update_data = {
                "name": name,
                "contact": contact,
                "date": date,
                "city": city,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            result = collection.update_one(
                {"reservation_id": reservation_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                dispatcher.utter_message(text="✅ Reservation updated successfully!")
            else:
                dispatcher.utter_message(text="❌ No reservation found to update.")
            
            return []
                
        except Exception as e:
            dispatcher.utter_message(text="Error updating reservation.")
            return []
        
class CancelReservation(Action):
    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            _: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        reservation_id = tracker.get_slot("reservation_id")

        client = MongoClient("mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/")
        db = client["pizza-bot"]
        collection = db["reservations"]
        
        
        result = collection.delete_one({"reservation_id": reservation_id})
        if result.deleted_count > 0:
                dispatcher.utter_message(text="✅ Reservation cancelled successfully!")
        else:
                dispatcher.utter_message(text="❌ Error cancelling reservation.")
        return [SlotSet("reservation_id", None)]
                    
