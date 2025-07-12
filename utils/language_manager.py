import json
import os

class LanguageManager:
    def __init__(self):
        self.language_data = {}
        self.current_lang = None
        # Default to English if a specific language file fails to load
        self.load_language('en') 

    def load_language(self, lang_code):
        """Loads a language file from the 'languages' directory."""
        path = os.path.join("languages", f"{lang_code}.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.language_data = json.load(f)
                self.current_lang = lang_code
                print(f"Successfully loaded language: {lang_code}")
        except FileNotFoundError:
            print(f"Error: Language file not found at {path}")
            # Fallback to English if the chosen language is not found
            if self.current_lang is None:
                self.load_language('en')

    def get(self, key):
        """Gets a string for the given key in the current language."""
        return self.language_data.get(key, f"<{key}>") # Return key in angle brackets if not found

    def get_specialty(self, key):
        """Gets a translated specialty name."""
        return self.language_data.get("specialties", {}).get(key, key)