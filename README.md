# AnkiAPI

A simple Python wrapper for interacting with the AnkiConnect API to create and manage Anki flashcards programmatically.

## Overview

AnkiAPI provides a clean interface to interact with Anki through the AnkiConnect add-on. It allows you to:

- Create new decks
- Add flashcards to decks
- Add audio media to Anki
- Test connectivity to the Anki application

## Prerequisites

1. [Anki](https://apps.ankiweb.net/) application installed
2. [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed in Anki

## Installation

```bash
pip install ankiapi
```

Or with Poetry:

```bash
poetry add ankiapi
```

## Usage

### Basic Example

```python
from ankiapi import AnkiApi

# Initialize the API (make sure Anki is running with AnkiConnect add-on)
anki = AnkiApi()

# Create a new deck
anki.create_deck("Python Programming")

# Add a flashcard
anki.add_flashcard(
    deck_name="Python Programming",
    front="What is a Python list comprehension?",
    back="A concise way to create lists using a single line of code with a for loop and optional conditions."
)
```

### Adding Audio to Anki

```python
# Add an audio file
anki.add_audio(
    path="/path/to/audio/file.mp3",
    filename="pronunciation.mp3"
)
```

## API Reference

### AnkiApi

```python
AnkiApi(url="http://localhost:8765", version=6)
```

The main class for interacting with the AnkiConnect API.

#### Parameters

- `url` (str): The URL of the AnkiConnect API. Default is "http://localhost:8765".
- `version` (int): The version of the AnkiConnect API. Default is 6.

#### Methods

##### check_server()

Checks whether the AnkiConnect server is running.

##### create_deck(deck_name)

Creates a new deck in Anki if it doesn't already exist.

- `deck_name` (str): The name of the deck to create.

##### add_flashcard(deck_name, front, back)

Adds a flashcard to the specified deck in Anki.

- `deck_name` (str): The name of the deck to add the card to.
- `front` (str): The content for the front side of the card.
- `back` (str): The content for the back side of the card.

##### add_audio(path, filename)

Adds media content to Anki.

- `path` (str): The path to the media file.
- `filename` (str): The filename to use for the media file in Anki.

## Troubleshooting

1. Make sure Anki is running before using the API
2. Ensure AnkiConnect add-on is properly installed
3. Check that you're using the correct port (default: 8765)

## License

See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.