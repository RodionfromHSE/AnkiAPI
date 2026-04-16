import json
import requests
from warnings import warn

# 127.0.0.1 instead of localhost: AnkiConnect binds to IPv4. Using "localhost"
# risks resolving to IPv6 and hitting unrelated processes on the same port.
_DEFAULT_URL = "http://127.0.0.1:8765"


class AnkiApi:
    """A class to interact with the AnkiConnect API."""

    def __init__(self, url: str = _DEFAULT_URL, version: int = 6):
        if url != _DEFAULT_URL:
            warn(
                f"Non-default AnkiConnect URL: {url}. "
                f"Default is {_DEFAULT_URL} (IPv4) to avoid IPv6 resolution issues.",
                stacklevel=2,
            )
        self.url = url
        self.version = version
        self.check_server()

    def check_server(self) -> None:
        """Verify the endpoint is a real AnkiConnect server (not just any HTTP 200)."""
        try:
            resp = requests.post(
                self.url,
                json={"action": "version", "version": self.version},
                timeout=2,
            )
            resp.raise_for_status()
            data = resp.json()
            if "result" not in data or data.get("error") is not None:
                raise ValueError("Not a valid AnkiConnect response")
            print("AnkiConnect is running")
        except Exception:
            raise RuntimeError(
                "Can't connect to Anki. Maybe you forgot to open Anki "
                "or to download the needed extension?"
            )

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