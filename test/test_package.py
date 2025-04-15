#!/usr/bin/env python
"""
Simple script to test the ankiapi package installation.
Note: Run this only if Anki is running with AnkiConnect add-on installed.
"""
try:
    from ankiapi import AnkiApi
    print("Successfully imported AnkiApi class from ankiapi package")
    
    # Optionally test connection (will raise error if Anki is not running)
    try:
        anki = AnkiApi()
        print("Successfully connected to Anki")
    except RuntimeError as e:
        print(f"Failed to connect to Anki: {e}")
        print("Make sure Anki is running with AnkiConnect add-on installed")
    
except ImportError as e:
    print(f"Failed to import AnkiApi: {e}")
    print("Make sure the package is installed correctly")
except Exception as e:
    print(f"An error occurred: {e}")