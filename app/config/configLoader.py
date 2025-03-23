import json
import os
import sys
from app import app

CONFIG = None  # Global variable for config

def load_config():
    """Loads the configuration file and sets it as a global variable."""
    global CONFIG
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    
    try:
        with open(config_path, "r") as config_file:
            CONFIG = json.load(config_file)
            app.logger.info("Config Successfully loaded!")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.logger.error(f"Error loading config file: {e}")
        CONFIG = None  # Set to None if loading fails
        sys.exit("Application terminated due to missing or invalid config file.")

# Load the config when the module is imported
load_config()
