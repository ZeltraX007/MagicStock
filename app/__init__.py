from flask import Flask
import logging
import json
from app.utils import logger
from app.config import dbConfig
import sys
import os
from pathlib import Path

# from app import configuration

app=Flask(__name__)

config_path = os.getenv("APP_CONFIG_PATH")
if config_path:
    config_path = Path(config_path)
else:
    config_path = Path(__file__).resolve().parents[1] / "backend" / "config.json"
    
try:
    with open(config_path, "r") as config_file:
        CONFIG = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    CONFIG = None  # Set to None if loading fails
    sys.exit("Application terminated due to missing or invalid config file.")

logger = logger.setup_logger(CONFIG.get("LOG_FILE_PATH", "app.log"))

#db connection
dbconnection = dbConfig.create_db_connection(CONFIG)


from controllers import controllers
## import services.stack_stock_service   # Uncomment this line if you want to fill data in stock list table
# import services.finantialScheduler 