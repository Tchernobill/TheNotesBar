import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "data/settings.json"

        # Default settings
        self.auto_hide = True
        self.always_on_top = True
        self.bar_position = "right"
        self.default_style = {
            "font": "Arial",
            "font_size": 12,
            "background_color": "#FFFFFF",
            "text_color": "#000000"
        }

        # Load settings from file if it exists
        self.load_settings()

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                data = json.load(file)
                self.auto_hide = data.get("auto_hide", self.auto_hide)
                self.always_on_top = data.get("always_on_top", self.always_on_top)
                self.bar_position = data.get("bar_position", self.bar_position)
                self.default_style = data.get("default_style", self.default_style)

    def save_settings(self):
        """Save the current settings to the JSON file."""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

        with open(self.settings_file, 'w') as file:
            json.dump({
                "auto_hide": self.auto_hide,
                "always_on_top": self.always_on_top,
                "bar_position": self.bar_position,
                "default_style": self.default_style
            }, file, indent=4)
