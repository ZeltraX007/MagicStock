from flask import request, jsonify
from app import app
import services.services as services
from app.config.configLoader import CONFIG

@app.route('/getStockRanks', methods=['POST'])
def stock_ranks():
    app.logger.info("Entering endpoint '/getStockRanks' route")

    incoming_header_value = request.headers.get(CONFIG.get("HEADER_KEY"))
    if incoming_header_value != CONFIG.get("HEADER_VALUE"):
        app.logger.warning("Unauthorized access attempt: Invalid header key or value")
        return jsonify({"error": "Unauthorized access"}), 401

    # Validate the header

    try:
        # Get JSON data from request
        result, err = services.getStockRanks(request.json, request.headers)
        
        if err:
            return jsonify({"status": "error", "message": str(err)}), 400

        response = {
            "status": "success",
            "totalStocks": len(result),
            "stocks": result
        }
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": "Invalid request"}), 400