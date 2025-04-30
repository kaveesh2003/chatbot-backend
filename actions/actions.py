from typing import Any, Text, Dict, List
import mysql.connector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# --- Helper Function to Connect to DB ---
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chathu@123",
        database="travel_db"
    )

# --- Action: Provide Travel Destinations ---
class ActionProvideDestinations(Action):
    def name(self) -> Text:
        return "action_provide_destinations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT name, description, category, district FROM destinations LIMIT 5")
            rows = cursor.fetchall()

            if rows:
                message = "Here are some popular destinations in Sri Lanka:\n"
                for name, description, category, district in rows:
                    message += f"\n🏞️ *{name}* ({category}, {district})\n{description}\n"
            else:
                message = "Sorry, I couldn't find any destinations at the moment."

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Database error: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return []

# --- Action: Provide Hotels ---
class ActionProvideHotels(Action):
    def name(self) -> Text:
        return "action_provide_hotels"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = """
                SELECT h.name, d.name AS destination_name, h.rating
                FROM hotels h
                JOIN destinations d ON h.destination_id = d.id
                ORDER BY h.rating DESC
                LIMIT 5
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                message = "Here are some recommended hotels:\n"
                for hotel_name, destination_name, rating in rows:
                    message += f"\n🏨 *{hotel_name}* near {destination_name} — ⭐ {rating}"
            else:
                message = "Sorry, I couldn't find any hotel data right now."

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Database error: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return []

# --- Action: Provide Travel Guidelines ---
class ActionProvideGuidelines(Action):
    def name(self) -> Text:
        return "action_provide_guidelines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT title, content FROM travel_guidelines LIMIT 5")
            rows = cursor.fetchall()

            if rows:
                message = "Here are some travel guidelines:\n"
                for title, content in rows:
                    message += f"\n📝 *{title}*:\n{content}\n"
            else:
                message = "No travel guidelines available at the moment."

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Database error: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        return []
