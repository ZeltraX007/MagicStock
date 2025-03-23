from app import app
from app.config.configLoader import CONFIG

if CONFIG is None:
    app.logger.error("Critical: Config file is missing or invalid. Shutting down.")
    exit(1)  # Ensures the app does not start

if __name__ == "__main__":
    app.run(debug=CONFIG.get("debug", True))
