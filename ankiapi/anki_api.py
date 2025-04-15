import json
import requests
from warnings import warn


class AnkiApi:
    """
    A class to interact with the AnkiConnect API.
    """
    def __init__(self, url: str = "http://localhost:8765", version: int = 6):
        """
        Initializes the AnkiAPI object.
        :@param url: The URL of the AnkiConnect API.
        :@param version: The version of the AnkiConnect API.
        """
        self.url = url
        self.version = version
        try:
            self.check_server()
        except Exception:
            # TODO: Make error output less verbose
            raise RuntimeError("Can't connect to Anki. Maybe you forgot to open Anki or to download the needed "
                               "extension?")

    def check_server(self):
        """Check whether the AnkiConnect server is running."""
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "ping",
            "version": self.version,
        }
        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print('AnkiConnect is running')
        except requests.exceptions.RequestException:
            raise RuntimeError('AnkiConnect is not running')

    def add_flashcard(self, deck_name, front, back):
        """
        Adds a flashcard to the specified deck in Anki.

        Args:
            deck_name (str): The name of the deck to add the card to.
            front (str): The content for the front side of the card.
            back (str): The content for the back side of the card.
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "addNote",
            "version": self.version,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front,
                        "Back": back
                    }
                }
            }
        }


        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            msg = result["error"]
            if "duplicate" in msg:
                warn(f"Flashcard '{front}' already exists in deck '{deck_name}'")
            else:
                raise Exception(result["error"])
        return result["result"]
    
    
    def add_audio(self, path: str, filename: str) -> None:
        """Add media content to Anki
        :@param path: The path to the media file
        :@param hash: The hash of the media file
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "storeMediaFile",
            "version": self.version,
            "params": {
                "filename": filename,
                "path": path
            }
        }
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            raise Exception(result["error"])
        return result["result"]

    def create_deck(self, deck_name: str) -> None:
        """
        Creates a new deck in Anki if it doesn't already exist.
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "createDeck",
            "version": self.version,
            "params": {
                "deck": deck_name
            }
        }

        # Send request to create deck
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        # Check response status and return result
        result = response.json()
        if result.get("error"):
            if result["error"] == "Deck already exists":
                print(f"Warning: Deck '{deck_name}' already exists.")
            else:
                raise Exception(result["error"])
        return result["result"]