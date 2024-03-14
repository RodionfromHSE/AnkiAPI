import json
import requests
from warnings import warn


class AnkiAPI:
    def __init__(self, url="http://localhost:8765", version=6):
        self.url = url
        self.version = version
        try:
            self.check_server()
        except Exception:
            # TODO: Make error output less verbose
            raise RuntimeError("Can't connect to Anki. Maybe you forgot to open Anki or to download the needed "
                               "extension?")

    def check_server(self):
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

    def add_flashcard(self, deck_name, front, back, path_to_audio=None):
        """
        Adds a flashcard to the specified deck in Anki.

        Args:
            deck_name (str): The name of the deck to add the card to.
            front (str): The content for the front side of the card.
            back (str): The content for the back side of the card.
            path_to_audio (str, optional): Path to an audio file to add to the back. Defaults to None.
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

        # Add audio if provided
        if path_to_audio:
            try:
                with open(path_to_audio, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                audio_base64 = audio_bytes.encode("base64").decode("utf-8")
                payload["params"]["note"]["fields"]["Back"] += f"<br>[sound:{audio_base64}]"
            except FileNotFoundError:
                warn(f"Audio file not found at: {path_to_audio}")

        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            raise Exception(result["error"])
        return result["result"]

    def create_deck(self, deck_name):
        # Connect to AnkiConnect API
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