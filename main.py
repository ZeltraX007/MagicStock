from app import app
from app.config.configLoader import CONFIG

if CONFIG is None:
    app.logger.error("Critical: Config file is missing or invalid. Shutting down.")
    exit(1)  # Ensures the app does not start

#TODO: Add a cookies system that would allow users to save their portfolio and compare it with the Magic Formula stocks.
if __name__ == "__main__":
    app.run(host=CONFIG.get("HOST","0.0.0.0"), port=CONFIG.get("PORT",8080), debug=CONFIG.get("DEBUG", True),use_reloader=False)