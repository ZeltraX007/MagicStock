from flask import Flask
import logging
import json
from app.utils import logger
from app.config import dbConfig
import sys
import os

# from app import configuration

app=Flask(__name__)

logger = logger.setup_logger()
logger.info("Flask application initialized.")

config_path = os.path.join(os.path.dirname(__file__), "./config/config.json")
    
try:
    with open(config_path, "r") as config_file:
        CONFIG = json.load(config_file)
        logger.info("Config Successfully loaded!")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Error loading config file: {e}")
    CONFIG = None  # Set to None if loading fails
    sys.exit("Application terminated due to missing or invalid config file.")

#db connection
dbconnection = dbConfig.create_db_connection(CONFIG)


from controllers import controllers
import services.stack_stock_service